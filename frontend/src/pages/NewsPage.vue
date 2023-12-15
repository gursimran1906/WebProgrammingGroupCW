<template>
  <div class="container mt-2">
    <!-- Check if articles are available -->
    <div v-if="articles.length > 0">
      <!-- Iterate over articles and display each article in a card -->
      <div
        v-for="article in articles"
        :key="article.id"
        class="card mb-3 shadow"
      >
        <!-- Card Header with article title and category -->
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

        <!-- Card Body with article content -->
        <div class="card-body">
          <p class="card-text">{{ article.content }}</p>
        </div>

        <!-- Card Footer with CommentForm and CommentsSection -->
        <div class="card-footer">
          <!-- CommentForm component with articleId prop and event handler -->
          <CommentForm
            :articleId="article.id"
            :placeholder="'Comment to Article'"
            @commentAdded="handleCommentAdded(article.id)"
          />

          <!-- Display comments using CommentsSection component -->

          <CommentsSection
            :commentReload="article.commentReload"
            :article-id="article.id"
          />
        </div>
      </div>
    </div>

    <!-- Display message if no articles are available -->
    <div v-else>
      <p>No articles available. Please choose My News under profile page.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import CommentsSection from "../components/CommentSection.vue";
import CommentForm from "../components/CommentForm.vue";

// Define the Article interface
interface Article {
  id: number;
  title: string;
  category: string;
  content: string;
  commentReload: boolean;
}

export default defineComponent({
  name: "NewsPage",
  components: {
    CommentsSection,
    CommentForm,
  },
  data() {
    return {
      articles: [] as Article[], // Array to store articles
    };
  },
  methods: {
    // Fetch articles from the API
    async fetchArticles(): Promise<void> {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/news/"); // Replace with your actual API endpoint
        const data = await response.json();

        // Map articles and add commentReload property
        this.articles = data.articles.map((article: Article) => ({
          ...article,
          commentReload: false,
        }));
      } catch (error) {
        console.error("Error fetching articles:", error);
      }
    },

    // Handle comment added event and update commentReload property
    handleCommentAdded(articleId: number): void {
      const articleIndex = this.articles.findIndex(
        (article) => article.id === articleId
      );
      if (articleIndex !== -1) {
        this.articles[articleIndex].commentReload =
          !this.articles[articleIndex].commentReload;
      }
    },
  },
  mounted() {
    // Fetch articles when the component is mounted
    this.fetchArticles();
  },
});
</script>
