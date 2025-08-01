import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      // Dev convenience: hit the FastAPI app on :8080 without CORS
      '/healthz': 'http://localhost:8080',
      '/metrics': 'http://localhost:8080',
      '/config': 'http://localhost:8080',
      '/dryrun': 'http://localhost:8080',
      '/webhooks': 'http://localhost:8080'
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
});