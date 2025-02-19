const path = require('path');
const { getSentryExpoConfig } = require('@sentry/react-native/metro');

// Get the Sentry/Expo config
const config = getSentryExpoConfig(__dirname);

// --- Add SVG support ---
// Tell Metro to use the SVG transformer for .svg files.
config.transformer = {
  ...config.transformer,
  babelTransformerPath: require.resolve('react-native-svg-transformer'),
};

// Remove 'svg' from assetExts and add it to sourceExts so that Metro
// processes SVG files as components rather than templates assets.
if (config.resolver && config.resolver.assetExts) {
  config.resolver.assetExts = config.resolver.assetExts.filter(ext => ext !== 'svg');
} else {
  config.resolver = config.resolver || {};
  config.resolver.assetExts = [];
}

config.resolver.sourceExts = [
  ...(config.resolver.sourceExts || []),
  'svg',
];

// --- Add custom path aliases ---
config.resolver.extraNodeModules = {
  ...config.resolver.extraNodeModules,
  '$app': path.resolve(__dirname, 'app'),
  '$shared': path.resolve(__dirname, 'shared'),
  '$features': path.resolve(__dirname, 'features'),
  '$entities': path.resolve(__dirname, 'entities'),
  '$widgets': path.resolve(__dirname, 'widgets'),
  '$pages': path.resolve(__dirname, 'pages'),
  '$assets': path.resolve(__dirname, 'assets'),
};

module.exports = config;
