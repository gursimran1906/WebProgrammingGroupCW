<template>
  <div class="container my-4">
    <div v-if="comments.length > 0">
      <div v-for="comment in comments" :key="comment.id" class="mb-3">
        <div class="card">
          <div class="card-header d-flex justify-content-between">
            <div class="card-title">
              <h5 class="inline">Comment by: {{ comment.user }}</h5>
            </div>
            <div class="card-title">
              <p class="inline text-right">
                Date: <b>{{ formatDateTime(comment.publication_date) }}</b>
              </p>
            </div>
          </div>
          <div class="card-body">
            <!-- Display comment content, user, etc. as needed -->
            <p class="card-text">{{ comment.content }}</p>

            <!-- Add more fields as needed -->
          </div>
        </div>
        <CommentForm
          :commentId="comment.id"
          :placeholder="comment.user"
          @commentAdded="fetchComments"
        />
      </div>
    </div>
    <div v-else>
      <p class="card-text">No comments available.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import CommentForm from "./CommentForm.vue";

export default defineComponent({
  name: "Comments",
  components: {
    CommentForm,
  },
  props: {
    articleId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      comments: [] as any[],
    };
  },
  methods: {
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
    // Fetch comments from the backend based on article ID
    async fetchComments() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/get_comments/${this.articleId}`
        );
        const data = await response.json();
        this.comments = data.comments;
        console.log(this.comments);
      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    },
  },
  mounted() {
    this.fetchComments();
  },
});
</script>

<style scoped>
/* Add your custom styles or Bootstrap classes here */
</style>
