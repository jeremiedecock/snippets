https://dev.to/jiprochazka/starting-up-a-new-vue-3-project-with-vite-and-docker-3355

```
docker-compose up -d
docker exec -it vuejs_snippets /bin/bash
```

Then follow these instructions to install Vuejs (c.f. https://vuejs.org/guide/quick-start.html#local) :

```
npm init vue@latest
chown -R 1010:1010 hello
cd hello/
```

Here, it's assumed that you create a project named "hello" and that your UID is 1010 ; adapt commands to your setup. 

Then, open the vite.config.js file and add the server object with the port field to the configuration:
```
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  server: {    // <-- this object is added
    port: 8001
  },
  plugins: [vue()]
})
```

We must also add parameter --host to the vite command in the package.json, so replace dev command in scripts:
```
// package.json
...
"scripts": {
    "dev": "vite --host",
...
```

Finally type:

```
npm install
npm run dev
```