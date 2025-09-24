
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
      pathRewrite: {
        '^/api': '/api'
      },
      onError: function (err, req, res) {
        console.log('Proxy Error:', err);
        res.writeHead(500, {
          'Content-Type': 'text/plain'
        });
        res.end('Proxy Error: Could not connect to backend server');
      }
    })
  );
};
