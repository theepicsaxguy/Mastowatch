import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// In Docker development, proxy to the API service directly
const proxyTarget = 'http://api:8080';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: {
      '/healthz': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/metrics': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/config': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/dryrun': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/webhooks': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/analytics': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/rules': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/admin': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/auth': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/scanning': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      },
      '/api': {
        target: proxyTarget,
        changeOrigin: true,
        cookieDomainRewrite: false,
        preserveHeaderKeyCase: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
});
