<template>
    <v-app>
      <v-container ma-24>
          <v-col>

            <v-textarea
              v-model="content"
              label="您的意见对我们很重要!💖"
              outlined
              class="pa-12"
              centered
              append-icon="mdi-comment"
              rows="10"
              no-resize
            >
              <template v-slot:append>
                <v-btn @click="submit" :disabled="content==''" color="primary">
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
      content:  '',
    }),

    methods: {
      submit() {
        if (this.content=='') {
          this.$message("不能为空哦")
        }
        else {
          var data = {
            content: this.content
          }
          console.log(data)
          feedback(this.$store.getters.uid, data).then(res => {
            this.$message('提交成功！感谢您的反馈！补锅侠已经在路上啦！😃')
            this.content = ''
            console.log(res)
            }).catch(error => {
            console.log(error)
          })
        }
      }
    }
  }
</script>
