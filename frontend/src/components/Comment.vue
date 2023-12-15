<template>
  <!-- Main container for a comment -->
  <div class="mb-3">
    <div class="card">
      <div class="card-header d-flex justify-content-between">
        <div class="card-title">
          <!-- Display user who made the comment -->
          <h5 class="inline">Comment by: {{ comment.user }}</h5>
        </div>
        <div class="card-title">
          <!-- Display the publication date of the comment -->
          <p class="inline text-right">
            Date: <b>{{ formatDateTime(comment.publication_date) }}</b>
          </p>
        </div>
      </div>
      <div v-if="!toggleEdit" class="card-body">
        <!-- Display the comment content if not in edit mode -->
        <p class="card-text">{{ comment.content }}</p>
      </div>
      <div v-if="toggleEdit" class="card-body">
        <!-- EditComment component for editing the comment -->
        <EditComment :comment="comment" @edited="handleCommentAdded" />
      </div>
      <div v-if="isCommentOwner(comment)" class="d-flex justify-content-end">
        <!-- Toggle between edit and cancel edit for the comment owner -->
        <a
          class="text-decoration-none pr-2"
          @click="toggleEdit = !toggleEdit"
          @mouseover="changeCursorOnHover"
          @mouseleave="resetCursor"
        >
          {{ toggleEdit ? "Cancel" : "Edit Comment" }}
        </a>
        &nbsp;|&nbsp;
        <a
          class="text-decoration-none pr-2"
          @click="deleteComment(comment.id)"
          @mouseover="changeCursorOnHover"
          @mouseleave="resetCursor"
        >
          Delete Comment</a
        >
      </div>

      <div v-if="childComments && childComments.length > 0">
        <!-- Display child comments using the ChildComment component -->
        <ChildComment
          v-for="comment in childComments"
          :key="comment.id"
          :comment="comment"
          @commentAdded="handleCommentAdded"
        />
      </div>

      <!-- CommentForm component for adding replies to the comment -->
      <div class="m-2">
        <CommentForm
          :comment-id="comment.id"
          @commentAdded="handleCommentAdded"
          :placeholder="'Reply to Comment'"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import CommentForm from "./CommentForm.vue";
import ChildComment from "./ChildComment.vue";
import EditComment from "./EditComment.vue";
import { useUserStore } from "../store";

interface UserDetails {
  profile_image: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
}

interface Comment {
  id: number;
  content: string;
  publication_date: string;
  user: string;
  // Add other properties as needed
}
export default defineComponent({
  name: "Comment",
  components: {
    CommentForm,
    EditComment,
    ChildComment,
  },
  data() {
    return {
      user: {} as UserDetails | null,
      toggleEdit: false,
    };
  },
  mounted() {
    // Fetch user details when the component is mounted
    this.fetchUserDetails();
  },
  props: {
    // Prop for the comment data
    comment: {
      type: Object as () => Comment,
      required: true,
    },
    // Prop for child comments array
    childComments: {
      type: Array as () => Comment[],
      required: false,
    },
  },
  methods: {
    deleteComment(commentID: number): void {
      const confirmDelete = window.confirm(
        "Are you sure you want to delete this comment?"
      );

      if (!confirmDelete) {
        // If the user cancels the deletion, you can choose to do nothing or show a message
        alert("Deletion canceled");
        return;
      }
      const deleteEndpoint = `http://127.0.0.1:8000/api/comment/${commentID}/delete/`;

      // Assuming you are using the Fetch API
      fetch(deleteEndpoint, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to delete comment");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);

          this.$emit("CommentAdded");
        })
        .catch((error) => {
          console.error("Error deleting comment:", error);

          // Display an error message or perform any other action
          alert("Failed to delete comment. Please try again.");
        });
    },
    // Change cursor to pointer on hover
    changeCursorOnHover() {
      document.body.style.cursor = "pointer";
    },
    // Reset cursor when not hovering
    resetCursor() {
      document.body.style.cursor = "auto";
    },
    // Check if the user is the owner of the comment
    isCommentOwner(cmt: any): boolean {
      return cmt.user == this.user?.username;
    },
    // Fetch user details from the store
    async fetchUserDetails(): Promise<void> {
      try {
        const userStore = useUserStore();
        const userDetails = await userStore.getUserDetails;
        this.user = userDetails;
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    },
    // Handle comment added event
    handleCommentAdded() {
      this.$emit("CommentAdded");
      this.toggleEdit = false;
    },
    // Format timestamp to a readable date and time
    formatDateTime(timestamp: string): string {
      const options: Intl.DateTimeFormatOptions = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        timeZone: "Europe/London",
      };

      const formattedDate: string = new Date(timestamp).toLocaleString(
        "en-GB",
        options
      );
      return formattedDate;
    },
  },
});
</script>
