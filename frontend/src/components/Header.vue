<template>
  <header class="navbar navbar-expand-lg navbar-light bg-light p-5">
    <div class="container">
      <router-link to="/" class="navbar-brand">Group 36 News App</router-link>

      <div>
        <!-- Profile link -->
        <router-link to="/profile" class="navbar-brand">
          <font-awesome-icon icon="user" />
        </router-link>

        <!-- Logout button -->
        <a
          @mouseover="changeCursorOnHover"
          @mouseleave="resetCursor"
          class="text-decoration-none"
          @click="Logout"
        >
          Log Out
        </a>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios from "axios";

export default defineComponent({
  name: "Header",

  methods: {
    changeCursorOnHover() {
      // Change cursor type to pointer on hover
      document.body.style.cursor = "pointer";
    },
    resetCursor() {
      // Reset cursor type when not hovering
      document.body.style.cursor = "auto";
    },

    Logout() {
      axios
        .post("http://127.0.0.1:8000/signout/")
        .then(() => {
          alert("Logged out successfully!! ");
          window.location.href = "http://127.0.0.1:8000/";
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
});
</script>
