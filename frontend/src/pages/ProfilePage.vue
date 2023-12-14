<template>
  <div class="container mt-5">
    <h1>User Profile</h1>

    <!-- Show user information and edit button if not in edit mode -->
    <div v-if="!isEditMode && user">
      <div class="shadow card mb-3">
        <img
          class="card-img-top rounded m-2 shadow-sm"
          :src="`http://127.0.0.1:8000${user.profile_image}`"
          alt="Profile Image"
          style="width: 150px; height: 150px; object-fit: cover"
        />

        <div class="card-body">
          <p class="card-text"><strong>Email:</strong> {{ user.email }}</p>
          <p class="card-text">
            <strong>First Name:</strong> {{ user.first_name }}
          </p>
          <p class="card-text">
            <strong>Last Name:</strong> {{ user.last_name }}
          </p>
          <p class="card-text">
            <strong>Date of Birth:</strong> {{ user.date_of_birth }}
          </p>
        </div>

        <button @click="toggleEditMode" class="btn btn-primary m-2">
          Edit Profile
        </button>
      </div>
    </div>

    <!-- Show user information form and save/cancel buttons if in edit mode -->
    <div v-else>
      <!-- Include form fields for first_name, last_name, and photo -->
      <form class="shadow" v-if="user" @submit.prevent="saveProfileChanges">
        <div class="mb-3 s">
          <label for="first_name" class="form-label">First Name:</label>
          <input
            v-model="user.first_name"
            type="text"
            class="form-control"
            id="first_name"
            required
          />
        </div>

        <div class="mb-3">
          <label for="last_name" class="form-label">Last Name:</label>
          <input
            v-model="user.last_name"
            type="text"
            class="form-control"
            id="last_name"
            required
          />
        </div>

        <div class="mb-3">
          <label for="profile_image" class="form-label">Profile Photo:</label>
          <input
            type="file"
            id="profile_image"
            @change="handleFileChange"
            accept="image/*"
          />
          <img
            v-if="user.profile_image"
            :src="user.profile_image"
            alt="Profile Preview"
            class="mt-2"
          />
        </div>

        <div>
          <button type="submit" class="btn btn-primary mb-2 mr-2">
            Save Changes
          </button>
          <button
            @click="cancelEditMode"
            type="button"
            class="btn btn-secondary mb-2"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>

    <!-- Show loading message while fetching user preferences -->
    <div v-if="isLoading">Loading user preferences...</div>

    <!-- Show user preferences if not loading -->
    <div v-else>
      <div class="card mb-3 shadow">
        <div class="card-body">
          <h2 class="card-title">My News</h2>

          <div>
            <span
              class="mb-2 clickable"
              v-for="category in availableCategories"
              :key="category"
              @click="toggleCategorySelection(category)"
              @mouseover="changeCursorOnHover"
              @mouseleave="resetCursor"
            >
              <div
                :class="[
                  isSelected(category)
                    ? 'bg-primary bg-gradient p-2'
                    : 'bg-secondary bg-gradient p-2',
                ]"
                class="rounded fs-4 text-white shadow-sm"
              >
                {{ isSelected(category) ? "✓" : "+" }} {{ category }}
              </div>
              <br />
            </span>
          </div>

          <button @click="savePreferences" class="btn btn-primary mt-3">
            Save Preferences
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useCategoryStore } from "../store";
import { useUserStore } from "../store";

interface UserDetails {
  profile_image: string;
  email: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
}

export default defineComponent({
  data() {
    return {
      user: {} as UserDetails | null,
      isLoading: false,
      isEditMode: false,
      selectedCategories: [] as string[],
      fetchedUserPreferences: [] as string[],
      profileImageFile: null as File | null,
    };
  },
  mounted() {
    this.fetchUserPreferences();
    this.fetchUserDetails();
  },
  computed: {
    availableCategories(): string[] {
      const categoryStore = useCategoryStore();
      return categoryStore.getCategories || [];
    },
  },
  methods: {
    toggleEditMode(): void {
      this.isEditMode = !this.isEditMode;
    },

    async saveProfileChanges(): Promise<void> {
      try {
        const formData = new FormData();
        formData.append("first_name", this.user?.first_name || "");
        formData.append("last_name", this.user?.last_name || "");
        if (this.profileImageFile) {
          formData.append("profile_image", this.profileImageFile);
        }

        // Make the API call to save profile changes using formData
        const response = await fetch(
          "http://127.0.0.1:8000/api/update_profile/",
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();
        if (response.ok) {
          console.log("Profile saved successfully");
        } else {
          console.error("Error saving profile:", data.error);
        }
      } catch (error) {
        console.error("Error saving profile:", error);
      } finally {
        this.isEditMode = false;
      }
    },

    cancelEditMode(): void {
      // Reset form values and toggle back to view mode
      // ...

      this.isEditMode = false;
    },

    handleFileChange(event: Event): void {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files[0]) {
        this.profileImageFile = target.files[0];

        // Optionally, you can preview the image before saving
        const reader = new FileReader();
        reader.onload = (e) => {
          this.user!.profile_image = e.target!.result as string;
        };
        reader.readAsDataURL(this.profileImageFile);
      }
    },

    changeCursorOnHover() {
      // Change cursor type to pointer on hover
      document.body.style.cursor = "pointer";
    },
    resetCursor() {
      // Reset cursor type when not hovering
      document.body.style.cursor = "auto";
    },
    isSelected(category: string): boolean {
      return this.selectedCategories.includes(category);
    },
    toggleCategorySelection(category: string): void {
      if (this.selectedCategories.includes(category)) {
        this.selectedCategories = this.selectedCategories.filter(
          (c) => c !== category
        );
      } else {
        this.selectedCategories.push(category);
      }
    },

    async fetchUserDetails(): Promise<void> {
      try {
        const userStore = useUserStore();
        this.isLoading = true;
        const userDetails = await userStore.getUserDetails;
        this.user = userDetails;
        console.log(this.user);
      } catch (error) {
        console.error("Error fetching user details:", error);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchUserPreferences(): Promise<void> {
      try {
        this.isLoading = true;

        const response = await fetch(
          "http://127.0.0.1:8000/api/user_preferences/"
        );
        const data = await response.json();

        this.fetchedUserPreferences = data.favorite_categories || [];
        this.selectedCategories = [...this.fetchedUserPreferences];
      } catch (error) {
        console.error("Error fetching user preferences:", error);
      } finally {
        this.isLoading = false;
      }
    },

    async savePreferences(): Promise<void> {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/save_user_preferences/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              favorite_categories: this.selectedCategories,
            }),
          }
        );

        const data = await response.json();
        if (response.ok) {
          console.log("Preferences saved successfully");
        } else {
          console.error("Error saving preferences:", data.error);
        }
      } catch (error) {
        console.error("Error saving preferences:", error);
      }
    },
  },
});
</script>
