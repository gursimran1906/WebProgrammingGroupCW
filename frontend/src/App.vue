<template>
  <div>
    <Header />
    <main class="container pt-4">
      <RouterView class="flex-shrink-0" />
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { RouterView } from "vue-router";
import Header from "./components/Header.vue";
import axios from "axios";
import { useUserStore } from "./store";
import { useCategoryStore } from "./store"; // Import your category store

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const categoryStore = useCategoryStore(); // Create an instance of your category store

    // Fetch user details and categories on component mount
    onMounted(async () => {
      try {
        // Fetch user details
        const userResponse = await axios.get(
          "http://127.0.0.1:8000/api/user_details/"
        );
        userStore.setUserDetails(userResponse.data);

        // Fetch categories
        const categoryResponse = await axios.get(
          "http://127.0.0.1:8000/api/all_categories/"
        );
        categoryStore.setCategories(categoryResponse.data.categories);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    });

    return {};
  },
  components: { RouterView, Header },
  methods: {},
});
</script>

<style scoped></style>
