<template>
  <div>
    <!-- Comment Form -->
    <form @submit.prevent="submitComment" class="mt-2">
      <div class="mb-2">
        <!-- Comment Content Textarea -->
        <textarea
          v-model="content"
          id="content"
          class="form-control"
          rows="1"
          :placeholder="content ? '' : placeholder"
        ></textarea>
      </div>
      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "CommentForm",
  props: {
    articleId: {
      type: Number,
      required: false,
    },
    commentId: {
      type: Number,
      required: false,
    },
    placeholder: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      // State for comment content and URL string
      content: "",
      urlStr: "",
    };
  },
  methods: {
    // Method to submit a comment
    async submitComment() {
      // Set the URL based on the presence of articleId or commentId
      if (this.articleId) {
        this.urlStr = `http://127.0.0.1:8000/api/article/${this.articleId}/add_comment/`;
      } else if (this.commentId) {
        this.urlStr = `http://127.0.0.1:8000/api/comment/${this.commentId}/add_reply/`;
      } else {
        // Handle invalid articleId or commentId
        console.error("Invalid articleId or commentId");
        return;
      }

      try {
        // Make a POST request to add a comment
        const response = await fetch(this.urlStr, {
          method: "POST",
          body: JSON.stringify({ content: this.content }),
        });

        // Parse the response JSON
        const data = await response.json();

        if (data.success) {
          // Comment added successfully
          this.content = "";
          // Emit event to notify parent component about the added comment
          this.$emit("commentAdded");
        } else {
          // Handle failure to add comment
          console.error("Failed to add comment:", data.errors);
          alert("Error in adding comments!");
        }
      } catch (error) {
        // Handle errors in the process
        console.error("Error adding comment:", error);
        alert("Error in adding comments!");
      }
    },
  },
});
</script>
