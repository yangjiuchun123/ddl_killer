<template>
<v-app>
  <v-row justify="center">
    <v-col cols="10">
      <v-card>
        <v-card-title>
          <v-chip-group
            mandatory
            active-class="deep-purple--text text--accent-4"
          >
            <v-chip v-for="tag in tags" :key="tag" @click="choose(tag)">
              {{ tag }}
            </v-chip>
          </v-chip-group>
        </v-card-title>
        <v-card-text>
          <v-list rounded>
            <v-list-item-group v-model="model">
              <!-- <template v-for="(item, i) in items"> -->
                <v-list-item
                  :key="i"
                  :value="item"
                  v-for="(item, i) in items"
                  @click="readMsg(item)"
                >
                  <!-- <v-list-item-icon>
                    <v-icon v-text="item.icon"></v-icon>
                  </v-list-item-icon> -->
                  <v-list-item-content :class="[item.has_read?'font-weight-light':'font-weight-bold']">
                    <v-list-item-title v-text="item.title"></v-list-item-title>
                    <v-list-item-subtitle class="my-2">{{ item.content | ellipsis }}</v-list-item-subtitle>
                    <!-- <v-list-item-subtitle class="d-flex justify-end">发布时间: {{item.release_time}}</v-list-item-subtitle> -->
                    <v-list-item-subtitle>{{item.author}}   发布于: {{item.release_time}}</v-list-item-subtitle>
                  </v-list-item-content>
                   
                  <!-- <v-list-item-action>
                    <v-icon
                      @click="read(item)"
                    >mdi-pencil</v-icon>
                  </v-list-item-action> -->

                </v-list-item>
              <!-- </template> -->
            </v-list-item-group>
          </v-list>

          <!-- 阅读消息对话框 -->
          <v-dialog
            v-model="dialog"
            width="500"
          >
            <v-card>
              <v-card-title
                class="headline"
                primary-title
              >
                {{ msgOpened.title }}
              </v-card-title>

              <v-card-subtitle class="mt-3">
                {{ msgOpened.author }} 发布于 {{ msgOpened.release_time }}
              </v-card-subtitle>

              <v-card-text class="font-weight-medium">
                {{ msgOpened.content }}
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  text
                  @click="dialog = false"
                >
                  I accept
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</v-app>
</template>

<script>
export default {
  data: () => ({
    tags: [
      '未读',
      '已读',
      '团体',
      '分享'
    ],

    msgs: [],
    msgOpened: {
      title: '',
      content: '',
      release_time: '',
      author: 'No One'
    },
    dialog: false,

    items: [
        {
          title: '这是一则会议消息',
          content: '会议balabalabalabalabalabalabalabalabalabala',
          release_time: '2020-05-01',
          author: 'No One',
          has_read: false
        },
        {
          title: '这是一则分享通知',
          content: '分享balabalabalabalabalabala',
          release_time: '2020-05-01',
          author: 'No One',
          has_read: false
        },
        {
          title: '这是一则其他通知',
          content: '其他balabalabalabalabalabala',
          release_time: '2020-05-01',
          author: 'No One',
          has_read: false
        },
      ],
      model: 1
  }),
  filters: {
    ellipsis (value) {
      if (!value) return ''
      if (value.length > 20) {
        return value.slice(0,20) + '...'
      }
      return value
    }
  },
  created() {
    initialize()
  },
  methods: {
    initialize() {

      // todo: get data from backend and screen

    },
    choose(tag) {
      console.log(tag)
    },
    readMsg(item) {
      // console.log(item)
      item.has_read = true
      this.msgOpened = item
      this.dialog = true
      // todo: post backend to modify "has_read" term
    }
  }
}
</script>

<style>
</style>
