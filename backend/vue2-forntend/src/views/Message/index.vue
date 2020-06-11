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
              {{ tag.text }}
            </v-chip>
          </v-chip-group>
        </v-card-title>
        <v-card-text>
          <v-list flat rounded>
            <v-list-item-group v-model="model">
              <!-- <template v-for="(item, i) in items"> -->
                <v-list-item
                  v-for="(item, i) in items"
                  :key="i"
                  :value="item"
                  @click="readMsg(item)"
                >
                  <!-- <v-list-item-icon>
                    <v-icon v-text="item.icon"></v-icon>
                  </v-list-item-icon> -->
                  <v-list-item-content :class="[item.is_read?'font-weight-light':'font-weight-bold']">
                    <v-list-item-title v-text="item.title"></v-list-item-title>
                    <v-list-item-subtitle class="my-2">{{ item.content | ellipsis }}</v-list-item-subtitle>
                    <!-- <v-list-item-subtitle class="d-flex justify-end">发布时间: {{item.publish_time}}</v-list-item-subtitle> -->
                    <v-list-item-subtitle>{{item.publisher}}   发布于: {{item.publish_time}}</v-list-item-subtitle>
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
                {{ msgOpened.publisher }} 发布于 {{ msgOpened.publish_time }}
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
                  @click="closeDialog()"
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

  <!-- broadcast -->
  <v-row justify="center" v-if="$store.getters.uid === '17373492'">
    <v-dialog v-model="broadcastDialog" persistent max-width="600px">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          Broadcast
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Broadcast</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="broadMsg.title"
                  label="title"
                  outlined
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="broadMsg.content"
                  outlined
                  placeholder="可以通过@学号的方式定向发送信息，格式中不会新产生空格，如：@17373492@17373493跟你们说一件事"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="broadcastDialog = false">Close</v-btn>
          <v-btn color="blue darken-1" text @click="broadCast">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</v-app>
</template>

<script>
import { getMessage, readMessage, broadcastMessage } from '@/api/message'

export default {
  inject: ['reload'],
  data: () => ({
    tags: [
      {text: '未读', value: 'unread'},
      {text: '已读', value: 'read'},
      {text: '团体', value: 'group'},
      {text: '分享', value: 'resource'},
      {text: '系统', value: 'system'},
      {text: '作业', value: 'homework'}
    ],

    msgs: [],
    msgOpened: {
      title: '',
      content: '',
      publish_time: '',
      publisher: 'No One'
    },
    dialog: false,
    broadcastDialog: false,
    broadMsg: {
      title: '',
      content: ''
    },

    ctag: '', //short for current tag
    items: [],
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
    this.initialize()
  },
  methods: {
    initialize() {
      this.ctag = 'unread'
      getMessage(this.$store.getters.uid, this.ctag).then(res => {
        this.items = res.data
      })
    }, 
    choose(tag) {
      this.ctag = tag.value
      console.log(this.ctag)
      getMessage(this.$store.getters.uid, tag.value).then(res => {
        this.items = res.data
      })
    },
    readMsg(item) {
      console.log(item)
      // todo: post backend to modify "is_read" term
      readMessage(this.$store.getters.uid, item.mid).then(res => {
        console.log(res)
        item.is_read = true
        this.msgOpened = item
        this.dialog = true
      })
    },
    closeDialog() {
      this.dialog = false
      if (this.ctag=="unread") {
        getMessage(this.$store.getters.uid, this.ctag).then(res => {
          this.items = res.data
        })
        this.reload()
      }
    },
    broadCast() {
      console.log(this.broadMsg)
      // backed api
      broadcastMessage(this.$store.getters.uid, this.broadMsg).then(res => {
        location.reload();
      })
      this.broadcastDialog = false
    }

  }
}
</script>

<style>
</style>
