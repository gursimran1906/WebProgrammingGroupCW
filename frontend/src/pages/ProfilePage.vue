<template>
  <!-- User Profile Container -->
  <div class="container mt-5">
    <h1>User Profile</h1>

    <!-- Show user information and edit button if not in edit mode -->
    <div v-if="!isEditMode && user">
      <!-- User Profile Card -->
      <div class="shadow card mb-3">
        <!-- Profile Image -->
        <img
          class="card-img-top rounded m-2 shadow-sm"
          :src="`http://127.0.0.1:8000${user.profile_image}`"
          alt="Profile Image"
          style="width: 150px; height: 150px; object-fit: cover"
        />

        <!-- User Information -->
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

        <!-- Edit Profile Button -->
        <button @click="toggleEditMode" class="btn btn-primary m-2">
          Edit Profile
        </button>
      </div>
    </div>

    <!-- Show user information form and save/cancel buttons if in edit mode -->
    <div v-else>
      <!-- User Information Form -->
      <form class="p-2 shadow" v-if="user" @submit.prevent="saveProfileChanges">
        <!-- First Name Input -->
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

        <!-- Last Name Input -->
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
        <!-- Profile DOB Input -->
        <div class="mb-3">
          <label for="date_of_birth" class="form-label">Date of Birth:</label>
          <input
            v-if="isEditMode"
            v-model="user.date_of_birth"
            type="date"
            class="form-control"
            id="date_of_birth"
          />
          <p v-else class="card-text">
            <strong>Date of Birth:</strong> {{ user.date_of_birth }}
          </p>
        </div>
        <!-- Email Input -->
        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input
            v-model="user.email"
            type="email"
            class="form-control"
            id="email"
            required
          />
        </div>
        <!-- Profile Image Input -->
        <div class="mb-3">
          <label for="profile_image" class="form-label">Profile Photo:</label>
          <input
            type="file"
            id="profile_image"
            @change="handleFileChange"
            accept="image/*"
          />
          <!-- Profile Image Preview -->
          <img
            v-if="user.profile_image"
            :src="user.profile_image"
            alt="Profile Preview"
            class="mt-2"
          />
        </div>

        <!-- Save and Cancel Buttons -->
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
      <!-- User Preferences Card -->
      <div class="card mb-3 shadow">
        <div class="card-body">
          <h2 class="card-title">My News</h2>

          <!-- Category Selection Buttons -->
          <div>
            <span
              class="mb-2 clickable"
              v-for="category in availableCategories"
              :key="category"
              @click="toggleCategorySelection(category)"
              @mouseover="changeCursorOnHover"
              @mouseleave="resetCursor"
            >
              <!-- Category Button -->
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

          <!-- Save Preferences Button -->
          <button @click="savePreferences" class="btn btn-primary mt-1">
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

// Interface for user details
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
    // Computed property for available categories from the store
    availableCategories(): string[] {
      const categoryStore = useCategoryStore();
      return categoryStore.getCategories || [];
    },
  },
  methods: {
    // Toggle between view and edit mode
    toggleEditMode(): void {
      this.isEditMode = !this.isEditMode;
    },

    // Save profile changes to the server
    async saveProfileChanges(): Promise<void> {
      try {
        const formData = new FormData();
        formData.append("first_name", this.user?.first_name || "");
        formData.append("last_name", this.user?.last_name || "");

        formData.append("email", this.user?.email || "");
        if (this.profileImageFile) {
          formData.append("profile_image", this.profileImageFile);
        }

        formData.append("date_of_birth", this.user?.date_of_birth || "");

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
          console.log("Profile Saved!", data.file_name);
          if (this.user) {
            this.user.profile_image = "/api/media/" + data.file_name;
          }
        } else {
          console.error("Error saving profile:", data.error);
        }
      } catch (error) {
        console.error("Error saving profile:", error);
      } finally {
        this.isEditMode = false;
      }
    },

    // Cancel the edit mode and reset form values
    cancelEditMode(): void {
      // Reset form values and toggle back to view mode
      // ...

      this.isEditMode = false;
    },

    // Handle file change for the profile image
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

    // Change cursor to pointer on hover
    changeCursorOnHover() {
      document.body.style.cursor = "pointer";
    },

    // Reset cursor to default when not hovering
    resetCursor() {
      document.body.style.cursor = "auto";
    },

    // Check if a category is selected
    isSelected(category: string): boolean {
      return this.selectedCategories.includes(category);
    },

    // Toggle the selection of a category
    toggleCategorySelection(category: string): void {
      if (this.selectedCategories.includes(category)) {
        this.selectedCategories = this.selectedCategories.filter(
          (c) => c !== category
        );
      } else {
        this.selectedCategories.push(category);
      }
    },

    // Fetch user details from the server
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

    // Fetch user preferences from the server
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

    // Save user preferences to the server
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
          alert("Preferences updated!");
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
