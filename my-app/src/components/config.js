module.exports = {
  secret: "my.secret.key",
  resolve: {
    fallback: {
      "crypto": require.resolve("crypto-browserify"),
    },
  },
};