<template>
  <div class="mb-3">
    <textarea
      v-model="editedContent"
      class="form-control"
      rows="1"
      placeholder="Edit your comment..."
    ></textarea>
    <button @click="saveEdit" class="btn btn-primary mt-2">Save</button>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from "vue";

// Define props and emits with their types
const props = defineProps<{
  comment: {
    id: number;
    content: string;
    publication_date: string;
    user: string;
  };
}>();
const emits = defineEmits(["edited"]);

// Define ref for edited content and comment id
const editedContent = ref<string>(props.comment.content);
const comment_id = ref<number>(props.comment.id);

// Define function to save edits
const saveEdit = async () => {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/comment/${comment_id.value}/edit_comment/`,
      {
        method: "POST",
        body: JSON.stringify({ content: editedContent.value }),
      }
    );

    const data = await response.json();

    if (data.success) {
      editedContent.value = "";
      emits("edited");
    } else {
      console.error("Failed to edit comment:", data.errors);
      alert("Error in editing comment!");
    }
  } catch (error) {
    console.error("Error editing comment:", error);
    alert("Error in editing comment!");
  }
};
</script>
