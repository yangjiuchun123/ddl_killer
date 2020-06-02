<template>
    <v-app>
      <v-container ma-24>
          <v-col>

            <v-textarea
              v-model="feed"
              label="您的意见对我们很重要!💖"
              outlined
              class="pa-12"
              centered
              append-icon="mdi-comment"
              rows="10"
              no-resize
            >
              <template v-slot:append>
                <v-btn @click="submit" :disabled="feed==''" color="primary">
                  提交
                  <v-icon>mdi-reply</v-icon>
                </v-btn>
              </template>
            </v-textarea>

          </v-col>
      </v-container>
    </v-app>

</template>


<script>
  import {feedback} from '@/api/user';
  export default {
    data: () => ({
      feed:  '',
    }),

    methods: {
      submit() {
        if (this.feed=='') {
          this.$message("不能为空哦")
        }
        else {
          feedback(this.$store.getters.uid, this.feed).then(res => {
            this.$message('提交成功！感谢您的反馈！补锅侠已经在路上啦！😃')
            console.log(res)
            }).catch(error => {
            console.log(error)
          })
        }
      }
    }
  }
</script>
