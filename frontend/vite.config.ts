import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const apiUrl = process.env.VITE_API_URL;

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: {
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
