<template>
  <div class="container mt-2">
    <h1 class="mb-3">News Page</h1>
    <div v-if="articles.length > 0">
      <div
        v-for="article in articles"
        :key="article.id"
        class="card mb-3 shadow"
      >
        <div class="card-header d-flex justify-content-between">
          <div class="card-title">
            <h5 class="inline">{{ article.title }}</h5>
          </div>
          <div class="card-title">
            <p class="inline text-right">
              Category: <b>{{ article.category }}</b>
            </p>
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">{{ article.content }}</p>
        </div>
        <div class="card-footer">
          <p>Add Comment:</p>
          <CommentForm
            :articleId="article.id"
            :placeholder="article.title"
            @commentAdded="handleCommentAdded"
          />
          <p class="mt-2">Comments:</p>
          <Comments :key="commentKey" :article-id="article.id" />
        </div>
      </div>
    </div>
    <div v-else>
      <p>No articles available.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Comments from "../components/Comments.vue";
import CommentForm from "../components/CommentForm.vue";

export default defineComponent({
  name: "NewsPage",
  components: {
    Comments,
    CommentForm,
  },
  data() {
    return {
      commentKey: 0,
      articles: [] as any[], // Assuming the structure of your articles
    };
  },
  methods: {
    handleCommentAdded() {
      console.log("Comment added!");

      this.commentKey += 1;
    },
    async fetchArticles() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/news/"); // Replace with your actual API endpoint
        const data = await response.json();
        this.articles = data.articles;
      } catch (error) {
        console.error("Error fetching articles:", error);
      }
    },
  },
  mounted() {
    this.fetchArticles();
  },
});
</script>

<style scoped>
/* Add your custom styles or Bootstrap classes here */
</style>
