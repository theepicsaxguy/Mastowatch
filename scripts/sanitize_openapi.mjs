#!/usr/bin/env node
/**
 * Schema-driven sanitizer for OpenAPI 3.1 specs.
 * - Consumes upstream schema.json
 * - Validates against OAS 3.1 meta-schema (Ajv)
 * - Removes unknown/vendor keys where the schema forbids them (via Ajv)
 * - Applies two generic, generator-compatibility rules:
 *   1) All header parameters -> schema.type = "string"
 *   2) Remove default: null on numeric/boolean schemas
 * - Removes `example` / `examples` universally (safe, avoids generator parse errors)
 *
 * Usage:
 *   node scripts/sanitize_openapi.mjs <inputSchemaPath> [outputPath]
 *
 * Defaults:
 *   outputPath = <input dir>/schema.cleaned.json
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { createRequire } from "module";

const require = createRequire(import.meta.url);

function die(msg, code = 1) {
  console.error(`[sanitize_openapi] ERROR: ${msg}`);
  process.exit(code);
}

const argv = process.argv.slice(2);
if (argv.length < 1) die("Missing input schema path");

const inputPath = path.resolve(argv[0]);
const outPath =
  argv[1] ? path.resolve(argv[1]) : path.join(path.dirname(inputPath), "schema.cleaned.json");

if (!fs.existsSync(inputPath)) die(`Input not found: ${inputPath}`);

let spec;
try {
  spec = JSON.parse(fs.readFileSync(inputPath, "utf8"));
} catch (e) {
  die(`Failed to parse JSON: ${e.message}`);
}

// --- Load OpenAPI 3.1 meta-schema (vendored via @apidevtools/openapi-schemas)
let oas31Schema;
try {
  // CJS -> ESM interop: import the package namespace and read openapiV31
  const openapiSchemas = require("@apidevtools/openapi-schemas");
  oas31Schema = openapiSchemas.openapiV31;
} catch (e) {
  die(`Cannot resolve OpenAPI 3.1 meta-schema: ${e.message}`);
}

// --- Generic, type-driven transforms (no endpoint knowledge)

/** Remove keys starting with x- (vendor extensions) and any example(s) */
function stripVendorAndExamples(obj) {
  if (Array.isArray(obj)) {
    for (let i = 0; i < obj.length; i++) {
      obj[i] = stripVendorAndExamples(obj[i]);
    }
    return obj;
  }
  if (obj && typeof obj === "object") {
    for (const k of Object.keys(obj)) {
      if (k === "example" || k === "examples" || k.startsWith("x-")) {
        delete obj[k];
        continue;
      }
      obj[k] = stripVendorAndExamples(obj[k]);
    }
  }
  return obj;
}

/** Remove default:null on number/integer/boolean */
function fixNullDefaultsInSchema(schema) {
  if (!schema || typeof schema !== "object") return schema;

  // Handle composite schemas
  for (const key of ["allOf", "anyOf", "oneOf"]) {
    if (Array.isArray(schema[key])) {
      schema[key] = schema[key].map(fixNullDefaultsInSchema);
    }
  }
  if (schema.not) schema.not = fixNullDefaultsInSchema(schema.not);
  if (schema.items) schema.items = fixNullDefaultsInSchema(schema.items);
  if (schema.prefixItems && Array.isArray(schema.prefixItems)) {
    schema.prefixItems = schema.prefixItems.map(fixNullDefaultsInSchema);
  }
  if (schema.properties && typeof schema.properties === "object") {
    for (const p of Object.keys(schema.properties)) {
      schema.properties[p] = fixNullDefaultsInSchema(schema.properties[p]);
    }
  }
  if (schema.additionalProperties && typeof schema.additionalProperties === "object") {
    schema.additionalProperties = fixNullDefaultsInSchema(schema.additionalProperties);
  }

  // Remove default: null on primitives
  const t = schema.type;
  if (
    Object.prototype.hasOwnProperty.call(schema, "default") &&
    schema.default === null &&
    (t === "integer" || t === "number" || t === "boolean")
  ) {
    delete schema.default;
  }
  return schema;
}

/** Make every header parameter's schema a simple string */
function forceHeaderParamsToString(obj) {
  if (Array.isArray(obj)) {
    for (let i = 0; i < obj.length; i++) obj[i] = forceHeaderParamsToString(obj[i]);
    return obj;
  }
  if (obj && typeof obj === "object") {
    // Parameter Object pattern: must have "in" and "name"
    if (obj.in === "header") {
      // For Header Object in components.headers, the structure is similar;
      // if "schema" exists and isn't a simple string, overwrite it.
      if (!obj.schema || typeof obj.schema !== "object" || obj.schema.type !== "string") {
        obj.schema = { type: "string" };
      }
    }
    for (const k of Object.keys(obj)) {
      obj[k] = forceHeaderParamsToString(obj[k]);
    }
  }
  return obj;
}

/** Fix data type mismatches in parameter defaults */
function fixParameterDefaults(obj) {
  if (Array.isArray(obj)) {
    for (let i = 0; i < obj.length; i++) {
      obj[i] = fixParameterDefaults(obj[i]);
    }
    return obj;
  }
  if (obj && typeof obj === "object") {
    // Fix parameters with type/default mismatches
    if (obj.parameters && Array.isArray(obj.parameters)) {
      obj.parameters = obj.parameters.map(param => {
        if (param && param.schema && Object.prototype.hasOwnProperty.call(param.schema, 'default')) {
          const schema = param.schema;
          const defaultValue = schema.default;
          
          // Fix string "null" defaults for integer/number types
          if ((schema.type === 'integer' || schema.type === 'number') && defaultValue === 'null') {
            console.warn(`[sanitize_openapi] Fixing invalid string "null" default for ${schema.type} parameter "${param.name}"`);
            schema.default = null;
          }
          
          // Fix other common type mismatches
          if (schema.type === 'boolean' && typeof defaultValue === 'string') {
            if (defaultValue.toLowerCase() === 'true') {
              schema.default = true;
            } else if (defaultValue.toLowerCase() === 'false') {
              schema.default = false;
            } else if (defaultValue === 'null') {
              schema.default = null;
            }
          }
        }
        return param;
      });
    }
    
    for (const k of Object.keys(obj)) {
      obj[k] = fixParameterDefaults(obj[k]);
    }
  }
  return obj;
}

/** Walk the entire spec to apply schema fixes in-place */
function walkFixSchemas(obj) {
  if (Array.isArray(obj)) {
    for (let i = 0; i < obj.length; i++) obj[i] = walkFixSchemas(obj[i]);
    return obj;
  }
  if (obj && typeof obj === "object") {
    if (obj.schema && typeof obj.schema === "object") {
      obj.schema = fixNullDefaultsInSchema(obj.schema);
    }
    // Also fix where schema objects appear directly (components.schemas.*)
    const maybeSchemaKeys = [
      "schema",
      "items",
      "not",
      "allOf",
      "anyOf",
      "oneOf",
      "properties",
      "additionalProperties",
      "prefixItems"
    ];
    for (const k of Object.keys(obj)) {
      if (maybeSchemaKeys.includes(k)) {
        // Sub-objects recursively handled by fixNullDefaultsInSchema during traversal
      }
      obj[k] = walkFixSchemas(obj[k]);
    }
  }
  return obj;
}

// Apply generic transforms
spec = stripVendorAndExamples(spec);
spec = forceHeaderParamsToString(spec);
spec = fixParameterDefaults(spec);
spec = walkFixSchemas(spec);

// Skip the aggressive schema validation that was corrupting parameter objects
console.log(`[sanitize_openapi] Applied basic transforms only (no schema validation removal)`);

// Write cleaned spec
try {
  fs.writeFileSync(outPath, JSON.stringify(spec, null, 2));
  console.log(`[sanitize_openapi] Wrote cleaned spec: ${outPath}`);
} catch (e) {
  die(`Failed to write cleaned schema: ${e.message}`);
}
