<template>
  <div>
    <form @submit.prevent="submitComment" class="mt-2">
      <div class="mb-2">
        <textarea
          v-model="content"
          id="content"
          class="form-control"
          rows="1"
          :placeholder="content ? '' : 'Comment/Reply to ' + placeholder"
        ></textarea>
      </div>
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
      content: "",
      urlStr: "",
    };
  },
  methods: {
    async submitComment() {
      if (this.articleId) {
        this.urlStr = `http://127.0.0.1:8000/api/article/${this.articleId}/add_comment/`;
      } else if (this.commentId) {
        this.urlStr = `http://127.0.0.1:8000/api/comment/${this.commentId}/add_reply/`;
      } else {
        console.error("Invalid articleId or commentId");
        return;
      }
      try {
        const response = await fetch(this.urlStr, {
          method: "POST",

          body: JSON.stringify({ content: this.content }),
        });
        console.log(this.content);
        const data = await response.json();

        if (data.success) {
          // Comment added successfully

          this.content = "";
          this.$emit("commentAdded");
        } else {
          console.error("Failed to add comment:", data.errors);
          alert("Error in adding comments!");
        }
      } catch (error) {
        console.error("Error adding comment:", error);
        alert("Error in adding comments!");
      }
    },
  },
});
</script>
