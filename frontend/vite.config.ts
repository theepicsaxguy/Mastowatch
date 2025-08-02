import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The API URL for browser requests - always localhost:8080 since we use Docker port mapping
const apiUrl = 'http://localhost:8080';

export default defineConfig({
  plugins: [react()],
  define: {
    // Make API URL available to frontend code
    'import.meta.env.VITE_API_URL': JSON.stringify(apiUrl),
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: {
      // Dev convenience: hit the FastAPI app on :8080 without CORS
      '/healthz': apiUrl,
      '/metrics': apiUrl,
      '/config': apiUrl,
      '/dryrun': apiUrl,
      '/webhooks': apiUrl,
      '/analytics': apiUrl,
      '/rules': apiUrl,
      '/admin': apiUrl,
      '/api': apiUrl
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
});