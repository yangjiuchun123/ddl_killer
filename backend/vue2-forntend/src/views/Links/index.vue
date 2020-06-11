<template>
    <v-app  class="Links-container">
      <v-banner>技术博客</v-banner>
      <v-container >
        <template>
         <v-row>
           <v-col cols="4" style="padding:20px">
             <!-- 站内跳转router-link，站外跳转a -->
             <a href="https://www.baidu.com" target="_blank" rel="noopener noreferrer">
              <v-hover
                v-slot:default="{ hover }"
                close-delay="200"
              >
                <v-card
                    :elevation="hover ? 16 : 2"
                    class="mx-auto"
                    color="#26c6da"
                    dark
                    max-width="400"
                  >
                    <v-card-title>
                      <v-icon
                        large
                        left
                      >
                        mdi-message-text
                      </v-icon>
                      <span class="title font-weight-light">Baidu</span>
                    </v-card-title>

                    <v-card-text class="headline font-weight-bold">
                      "百度的使命：用科技让复杂的世界更简单.
                      百度的愿景：成为最懂用户，并能帮助人们成长的全球顶级高科技公司."
                    </v-card-text>

                    <v-card-actions>
                      <v-list-item class="grow">
                        <v-list-item-avatar color="grey darken-3">
                          <v-img
                            class="elevation-6"
                            src="https://i.niupic.com/images/2020/03/21/74sf.jpg"
                          ></v-img>
                        </v-list-item-avatar>

                        <v-list-item-content>
                          <v-list-item-title>李彦宏</v-list-item-title>
                        </v-list-item-content>

                      </v-list-item>
                    </v-card-actions>
                  </v-card>
              </v-hover>
            </a>  
           </v-col>
           <v-col cols="4" style="padding:20px">
             <!-- 站内跳转router-link，站外跳转a -->
             <a href="https://www.baidu.com" target="_blank" rel="noopener noreferrer">
              <v-hover
                v-slot:default="{ hover }"
                close-delay="200"
              >
                <v-card
                    :elevation="hover ? 16 : 2"
                    class="mx-auto"
                    color="#26c6da"
                    dark
                    max-width="400"
                  >
                    <v-card-title>
                      <v-icon
                        large
                        left
                      >
                        mdi-message-text
                      </v-icon>
                      <span class="title font-weight-light">Baidu</span>
                    </v-card-title>

                    <v-card-text class="headline font-weight-bold">
                      "百度的使命：用科技让复杂的世界更简单.
                      百度的愿景：成为最懂用户，并能帮助人们成长的全球顶级高科技公司."
                    </v-card-text>

                    <v-card-actions>
                      <v-list-item class="grow">
                        <v-list-item-avatar color="grey darken-3">
                          <v-img
                            class="elevation-6"
                            src="https://i.niupic.com/images/2020/03/21/74sf.jpg"
                          ></v-img>
                        </v-list-item-avatar>

                        <v-list-item-content>
                          <v-list-item-title>李彦宏</v-list-item-title>
                        </v-list-item-content>

                      </v-list-item>
                    </v-card-actions>
                  </v-card>
              </v-hover>
            </a>  
           </v-col>
           <v-col cols="4" style="padding:20px">
             <!-- 站内跳转router-link，站外跳转a -->
             <a href="https://www.baidu.com" target="_blank" rel="noopener noreferrer">
              <v-hover
                v-slot:default="{ hover }"
                close-delay="200"
              >
                <v-card
                    :elevation="hover ? 16 : 2"
                    class="mx-auto"
                    color="#26c6da"
                    dark
                    max-width="400"
                  >
                    <v-card-title>
                      <v-icon
                        large
                        left
                      >
                        mdi-message-text
                      </v-icon>
                      <span class="title font-weight-light">Baidu</span>
                    </v-card-title>

                    <v-card-text class="headline font-weight-bold">
                      "百度的使命：用科技让复杂的世界更简单.
                      百度的愿景：成为最懂用户，并能帮助人们成长的全球顶级高科技公司."
                    </v-card-text>

                    <v-card-actions>
                      <v-list-item class="grow">
                        <v-list-item-avatar color="grey darken-3">
                          <v-img
                            class="elevation-6"
                            src="https://i.niupic.com/images/2020/03/21/74sf.jpg"
                          ></v-img>
                        </v-list-item-avatar>

                        <v-list-item-content>
                          <v-list-item-title>李彦宏</v-list-item-title>
                        </v-list-item-content>

                      </v-list-item>
                    </v-card-actions>
                  </v-card>
              </v-hover>
            </a>  
           </v-col>
         </v-row>
      </v-container>
    </v-app>

</template>


<script>
  export default {
    data: () => ({
    }),

    methods:{

    }
  }
</script>


<style lang="scss" scoped>
  $bg:#2d3a4b;
  // $dark_gray:#889aa4;
  // $light_gray:#eee;
  $white: #ffffff;

  .Links-container {
    min-height: 100%;
    width: 100%;

    
    top: 0;
    left: 0;
    width:100%;
    height:100%;
    min-width: 1000px;
    z-index:-10;
    zoom: 1;
    background-color: #fff;
    background-repeat: no-repeat;
    background-size: cover;
    -webkit-background-size: cover;
    -o-background-size: cover;
    background-position: center 0;
    // background-color: $bg;
    overflow: hidden;
    
  }
</style>


