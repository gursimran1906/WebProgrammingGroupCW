import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import { createApp } from "vue";
import App from "./App.vue";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { createPinia } from "pinia";

library.add(faUser);

const app = createApp(App);
app.use(createPinia());
app.component("font-awesome-icon", FontAwesomeIcon);

app.use(router);

app.mount("#app");
