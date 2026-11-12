import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  // 앱인토스 콘솔에 등록한 앱 이름과 반드시 똑같아야 해요.
  appName: 'lovedecode',
  permissions: [],
  navigationBar: {
    withBackButton: true,
    withHomeButton: true,
    theme: 'dark',
  },
  webBundleDir: 'dist',
});
