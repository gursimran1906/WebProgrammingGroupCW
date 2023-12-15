<template>
  <!-- Main container for comments -->
  <div class="my-2">
    <div v-if="comments.length > 0">
      <!-- Render comments using the Comment component -->
      <Comment
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :childComments="getChildComments(comment.id)"
        @commentAdded="handleCommentAdded"
      />
    </div>
    <div v-else>
      <!-- Display message when no comments are available -->
      <p class="card-text">No comments available.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Comment from "./Comment.vue";

// Define interface for Comment object
interface Comment {
  id: number;
  content: string;
  publication_date: string;
  user: string;
}

export default defineComponent({
  name: "Comment Section",
  components: {
    Comment,
  },
  props: {
    // Props for triggering comment reload and article ID
    commentReload: {
      type: Boolean,
      required: true,
    },
    articleId: {
      type: Number,
      required: true,
    },
  },

  watch: {
    // Watch for changes in commentReload prop
    commentReload(): void {
      // Triggered when a new comment is added
      this.handleCommentAdded();
    },
  },
  data() {
    return {
      // State for storing comments and child comments
      comments: [] as Comment[],
      childComments: {} as Record<number, Comment[]>, // Use Record to specify the type of childComments
    };
  },
  methods: {
    // Method called when a new comment is added
    handleCommentAdded(): void {
      // Fetch updated child and parent comments
      this.fetchChildComments();
      this.fetchComments();
    },
    // Get child comments for a given parent ID
    getChildComments(parentID: number): Comment[] {
      const childComments = this.childComments[parentID];
      return childComments || [];
    },

    // Fetch parent comments for the article
    async fetchComments() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/get_comments/${this.articleId}`
        );
        const data = await response.json();
        // Update the comments array with fetched data
        this.comments = data.comments;
      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    },
    // Fetch child comments for the article
    async fetchChildComments() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/get_child_comments/${this.articleId}`
        );
        const data = await response.json();
        // Update the childComments object with fetched data
        this.childComments = data.child_comments;
      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    },
  },
  mounted() {
    // Fetch initial set of comments and child comments when component is mounted
    this.fetchComments();
    this.fetchChildComments();
  },
});
</script>
