import { defineStore } from "pinia";

interface UserDetails {
  // Define your user details structure here
  profile_image: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
}
export const useUserStore = defineStore({
  id: "user",
  state: () => ({
    userDetails: null as UserDetails | null,
  }),
  getters: {
    getUserDetails(): UserDetails | null {
      return this.userDetails;
    },
  },
  actions: {
    setUserDetails(details: UserDetails | null): void {
      this.userDetails = details;
    },
  },
});

interface CategoryState {
  categories: string[];
}

export const useCategoryStore = defineStore({
  id: "category",
  state: (): CategoryState => ({
    categories: [],
  }),
  getters: {
    getCategories(): string[] {
      return this.categories;
    },
  },
  actions: {
    setCategories(categories: string[]): void {
      this.categories = categories;
    },
  },
});
