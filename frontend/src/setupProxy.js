
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
      secure: false,
      logLevel: 'debug',
      timeout: 10000,
      proxyTimeout: 10000,
      onError: (err, req, res) => {
        console.error('Proxy error:', err);
        res.status(500).send('Proxy Error');
      },
      onProxyReq: (proxyReq, req, res) => {
        console.log(`Proxying ${req.method} ${req.path} to backend`);
      },
      onProxyRes: (proxyRes, req, res) => {
        console.log(`Backend responded with status: ${proxyRes.statusCode}`);
      }
    })
  );
};
