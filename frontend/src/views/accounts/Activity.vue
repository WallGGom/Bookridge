<template>
  <div id="main d-flex flex-row" class="my-5 bg mx-auto" style="max-width: 80%">
    <v-row no-gutters>
      <v-col md="6" offset-md="3">
        <v-divider></v-divider>
      </v-col>
    </v-row>
    <h1 class="do text-center mt-3">{{ name }}님의 독서 활동</h1>
    <v-row no-gutters>
      <v-col md="6" offset-md="3">
        <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-container class="mx-auto" style="min-width: 80%">
      <v-system-bar color="#004D40"> </v-system-bar>
      <!-- 독서 기록 -->
      <v-card id="bookLog" class="scrollme1">
        <v-card-text class="text-center">
          <v-row class="d-flex justify-content-center">
            <h2 class="my-5" style="font-family: HangeulNuri-Bold">
              📅{{ name }}님의 독서 기록
            </h2>
          </v-row>
          <v-row class="d-flex justify-content-end mr-5">
            <i style="color: red" class="fas fa-circle mt-1"></i>
            <p class="ml-1 mr-3 main-font">: 미완독</p>
            <i style="color: blue" class="fas fa-circle mt-1"></i>
            <p class="ml-1 main-font">: 완독</p>
          </v-row>
          <v-row class="d-flex justify-content-end">
            <v-dialog
              v-model="dialogCalendar"
              persistent
              max-width="900px"
              @keydown.esc="dialogCalendar = false"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  class="mr-5"
                  text
                  outlined
                  color="#006064"
                  v-bind="attrs"
                  v-on="on"
                  style="
                    font-family: HangeulNuri-Bold;
                    border-color: #006064;
                    border-width: 3px;
                  "
                  ><i class="fas fa-plus"></i>추가</v-btn
                >
              </template>

              <v-card width="900px">
                <v-card-title class="main-color justify-content-center">
                  <span
                    v-if="!isUpdate"
                    class="text-white"
                    style="font-family: HangeulNuri-Bold; font-size: x-large"
                    >도서 추가하기</span
                  >
                  <span
                    v-else
                    class="text-white"
                    style="font-family: HangeulNuri-Bold; font-size: x-large"
                    >도서 수정하기</span
                  >
                </v-card-title>
                <v-card-text>
                  <v-form ref="form" v-model="valid" lazy-validation>
                    <v-container>
                      <div v-if="!isSelected">
                        <v-row class="mt-5">
                          <v-text-field
                            v-model="searchWord"
                            @keyup="bookSearch"
                            label="도서 검색"
                            outlined
                            color="success"
                            clearable
                          ></v-text-field>
                        </v-row>
                        <v-row>
                          <v-col
                            v-for="book in autoBooks"
                            :key="book.id"
                            cols="4"
                            md="4"
                          >
                            <div class="card">
                              <v-img
                                v-if="book.img_url"
                                class="imgBx bookimage"
                                :src="book.img_url"
                              ></v-img>
                              <v-img
                                v-else
                                class="imgBx bookimage"
                                src="@/assets/img/no-image.jpg"
                              ></v-img>

                              <div class="details" style="height: 300px">
                                <div v-if="book.title">
                                  <h6 v-show="book.title.length > 10">
                                    {{ book.title.slice(0, 10) }}...
                                  </h6>
                                  <h6 v-show="book.title.length <= 10">
                                    {{ book.title }}
                                  </h6>
                                </div>
                                <div v-else>
                                  <h6>제목이 없는 책입니다.</h6>
                                </div>
                                <div
                                  v-if="book.description"
                                  style="height: 100px"
                                >
                                  <small v-show="book.description.length > 60">
                                    {{ book.description.slice(0, 60) }}...
                                  </small>
                                  <small v-show="book.description.length <= 60">
                                    {{ book.description }}
                                  </small>
                                </div>
                                <div v-else style="height: 100px">
                                  <small
                                    >줄거리에 대한 정보가 없는 책입니다.</small
                                  >
                                </div>
                                <v-row
                                  class="mt-5 d-flex justify-content-center"
                                >
                                  <v-btn
                                    text
                                    outlined
                                    color="white"
                                    @click="goToBookDetail(book.id)"
                                    class="main-font"
                                    >책 바로가기</v-btn
                                  >
                                  <v-btn
                                    text
                                    outlined
                                    color="success"
                                    @click="selectBook(book)"
                                    class="main-font"
                                    >선택</v-btn
                                  >
                                </v-row>
                              </div>
                            </div>
                          </v-col>
                        </v-row>
                      </div>
                      <div
                        v-else
                        class="d-flex justify-content-center flex-column"
                      >
                        <h3
                          style="font-family: HangeulNuri-Bold"
                          class="text-center"
                        >
                          {{ pickedBook.title }}
                        </h3>
                        <div class="d-flex justify-content-center">
                          <v-img
                            v-if="pickedBook.img_url"
                            contain
                            :src="pickedBook.img_url"
                            class="bookimage"
                          ></v-img>
                          <v-img
                            v-else
                            contain
                            src="@/assets/img/no-image.jpg"
                            class="bookimage"
                          ></v-img>
                        </div>
                        <p style="font-family: HangeulNuri-Bold">
                          {{ pickedBook.description }}
                        </p>

                        <v-row class="d-flex justify-content-center">
                          <v-btn
                            text
                            class="main-font"
                            color="warning"
                            @click="cancelSelect"
                            style="font-family: HangeulNuri-Bold"
                            >선택 취소</v-btn
                          >
                        </v-row>
                      </div>
                      <v-row class="mt-5">
                        <v-col cols="6">
                          <v-menu
                            ref="menuStart"
                            v-model="menuStart"
                            :close-on-content-click="false"
                            :return-value.sync="Sdate"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                color="success"
                                v-model="Sdate"
                                label="독서 시작 날짜"
                                required
                                readonly
                                :rules="[rules.startDate]"
                                v-bind="attrs"
                                v-on="on"
                                style="font-family: HangeulNuri-Bold"
                              ></v-text-field>
                            </template>
                            <v-date-picker
                              locale="south-korea"
                              v-model="Sdate"
                              no-title
                              scrollable
                              :max="SDateMax"
                              class="do"
                            >
                              <v-spacer></v-spacer>
                              <v-btn
                                text
                                color="success"
                                @click="$refs.menuStart.save(Sdate)"
                                style="font-family: HangeulNuri-Bold"
                                >확인</v-btn
                              >
                              <v-btn
                                text
                                color="error"
                                @click="menuStart = false"
                                style="font-family: HangeulNuri-Bold"
                                >취소</v-btn
                              >
                            </v-date-picker>
                          </v-menu>
                        </v-col>
                        <v-col cols="6">
                          <v-menu
                            ref="menuEnd"
                            v-model="menuEnd"
                            :close-on-content-click="false"
                            :return-value.sync="Edate"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                color="success"
                                v-model="Edate"
                                label="독서 마감 날짜"
                                required
                                readonly
                                v-bind="attrs"
                                v-on="on"
                                style="font-family: HangeulNuri-Bold"
                              ></v-text-field>
                            </template>
                            <v-date-picker
                              locale="south-korea"
                              v-model="Edate"
                              :min="EDateMin"
                              :max="EDateMax"
                              no-title
                              scrollable
                              style="font-family: HangeulNuri-Bold"
                            >
                              <v-spacer></v-spacer>
                              <v-btn
                                text
                                color="success"
                                @click="$refs.menuEnd.save(Edate)"
                                style="font-family: HangeulNuri-Bold"
                                >확인</v-btn
                              >
                              <v-btn
                                text
                                color="error"
                                @click="menuEnd = false"
                                style="font-family: HangeulNuri-Bold"
                                >취소</v-btn
                              >
                            </v-date-picker>
                          </v-menu>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-form>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    v-if="!isUpdate"
                    :disabled="!isSelected || !Sdate"
                    color="success"
                    text
                    @click="createCalendar"
                    style="font-family: HangeulNuri-Bold"
                    >저장</v-btn
                  >
                  <v-btn
                    v-else
                    :disabled="!isSelected || !Sdate"
                    color="success"
                    text
                    @click="updateCalendar"
                    style="font-family: HangeulNuri-Bold"
                    >수정</v-btn
                  >
                  <v-btn
                    style="font-family: HangeulNuri-Bold"
                    color="error"
                    text
                    @click="cancelCalendar"
                    >취소</v-btn
                  >
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
          <v-row>
            <v-date-picker
              locale="south-korea"
              color="#009688"
              v-model="date"
              full-width
              :landscape="$vuetify.breakpoint.smAndUp"
              :event-color="(date) => (date ? 'red' : 'yellow')"
              :events="calendarEvents"
              class="mt-4"
              style="font-family: HangeulNuri-Bold"
            ></v-date-picker>
          </v-row>
          <p v-show="!dailyBook" style="font-family: HangeulNuri-Bold">
            해당 날짜의 도서기록이 없습니다.
          </p>
        </v-card-text>
        <!-- <Calendar />> -->
        <v-row>
          <v-container fluid class="mt-5">
            <div v-if="todayBlueBook.length">
              <p
                class="text-center mb-0"
                style="
                  font-family: HangeulNuri-Bold;
                  font-size: x-large;
                "
              >
                🙆‍♀️ 완독 목록
              </p>
              <v-row no-gutters>
                <v-col md="2" offset-md="5">
                  <v-divider></v-divider>
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="3"
                  v-for="book in todayBlueBook"
                  :key="book.id"
                  class="py-0"
                >
                  <v-img
                    v-if="book.book.img_url"
                    class="imgBx bookimage cursor"
                    :src="book.book.img_url"
                    @click="goToBookDetail(book.book.id)"
                    uk-tooltip="책 상세보기"
                  ></v-img>
                  <v-img
                    v-else
                    class="imgBx bookimage cursor"
                    src="@/assets/img/no-image.jpg"
                    @click="goToBookDetail(book.book.id)"
                    uk-tooltip="책 상세보기"
                  ></v-img>

                  <p
                    style="
                      font-family: HangeulNuri-Bold;
                      font-size: small;
                      text-align: center;
                    "
                  >
                    {{ book.calendar.start_date }} ~
                    {{ book.calendar.end_date }}
                  </p>

                  <div
                    v-show="isYou"
                    style="display: flex; justify-content: center"
                  >
                    <v-btn
                      text
                      outlined
                      @click="deleteCalendar(book.calendar.id)"
                      style="
                        font-family: HangeulNuri-Bold;
                        color: red;
                        border-color: red;
                        border-width: 3px;
                      "
                    >
                      삭제
                    </v-btn>
                  </div>
                </v-col>
              </v-row>
            </div>
            <v-divider></v-divider>
            <div v-if="todayRedBook.length" style="top: 10%">
              <p
                class="text-center mb-0"
                style="
                  font-family: HangeulNuri-Bold;
                  font-size: x-large;
                "
              >
                🙅‍♀️ 미완독 목록
              </p>
              <v-row no-gutters>
                <v-col md="2" offset-md="5">
                  <v-divider></v-divider>
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="3"
                  v-for="book in todayRedBook"
                  :key="book.id"
                  class="py-0"
                >
                  <v-img
                    v-if="book.book.img_url"
                    class="imgBx bookimage cursor"
                    :src="book.book.img_url"
                    @click="goToBookDetail(book.book.id)"
                    uk-tooltip="책 상세보기"
                  ></v-img>
                  <v-img
                    v-else
                    class="imgBx bookimage cursor"
                    src="@/assets/img/no-image.jpg"
                    @click="goToBookDetail(book.book.id)"
                    uk-tooltip="책 상세보기"
                  ></v-img>

                  <p
                    style="
                      font-family: HangeulNuri-Bold;
                      font-size: small;
                      text-align: center;
                    "
                  >
                    {{ book.calendar.start_date }} ~
                  </p>

                  <div
                    v-show="isYou"
                    style="display: flex; justify-content: center"
                  >
                    <v-btn
                      text
                      outlined
                      @click="beforeUpdate(book)"
                      style="
                        font-family: HangeulNuri-Bold;
                        color: green;
                        border-color: green;
                        border-width: 3px;
                      "
                    >
                      수정
                    </v-btn>
                    <v-btn
                      text
                      outlined
                      @click="deleteCalendar(book.calendar.id)"
                      style="
                        font-family: HangeulNuri-Bold;
                        color: red;
                        border-color: red;
                        border-width: 3px;
                      "
                    >
                      삭제
                    </v-btn>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-container>
        </v-row>
      </v-card>

      <!-- 나의서재 -->

      <v-card id="bookShelf" class="scrollme2">
        <v-system-bar color="#004D40"> </v-system-bar>
        <v-card-text class="text-center">
          <v-row>
            <v-col>
              <h2 class="my-5" style="font-family: HangeulNuri-Bold">
                📚{{ name }}님의 서재
              </h2>
            </v-col>
          </v-row>
        </v-card-text>
        <v-tabs background-color="white" color="#009688" centered>
          <v-tab style="font-family: HangeulNuri-Bold">좋아요한 책</v-tab>
          <v-tab style="font-family: HangeulNuri-Bold">작성한 리뷰</v-tab>
          <v-tab style="font-family: HangeulNuri-Bold">작성한 글귀</v-tab>
          <!-- 좋아요한 책 -->
          <v-tab-item class="mt-5">
            <v-container fluid class="pb-0">
              <v-row v-if="alllikeBooks != '좋아요한 책이 없습니다.'">
                <v-col
                  v-for="(book, idx) in likeBooks"
                  :key="idx"
                  cols="3"
                  lg="3"
                  sm="6"
                  xs="6"
                  class="pt-0"
                >
                  <div class="card cursor">
                    <v-img
                      v-if="book.img_url"
                      class="imgBx bookimage"
                      :src="book.img_url"
                    ></v-img>
                    <v-img
                      v-else
                      class="imgBx bookimage"
                      src="@/assets/img/no-image.jpg"
                    ></v-img>

                    <div class="details">
                      <div v-if="book.title">
                        <h6
                          v-show="book.title.length > 10"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ book.title.slice(0, 10) }}...
                        </h6>
                        <h6
                          v-show="book.title.length <= 10"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ book.title }}
                        </h6>
                      </div>
                      <div v-else>
                        <h6 style="font-family: HangeulNuri-Bold">
                          제목이 없는 책입니다.
                        </h6>
                      </div>
                      <div v-if="book.description">
                        <small
                          v-show="book.description.length > 60"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ book.description.slice(0, 60) }}...
                        </small>
                        <small
                          v-show="book.description.length <= 60"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ book.description }}
                        </small>
                      </div>
                      <div v-else style="height: 100px">
                        <small style="font-family: HangeulNuri-Bold"
                          >줄거리에 대한 정보가 없는 책입니다.</small
                        >
                      </div>
                      <v-row class="mt-5 d-flex justify-content-center">
                        <v-btn
                          @click="goToBookDetail(book.id)"
                          text
                          outlined
                          color="white"
                          class="mt-3"
                          style="font-family: HangeulNuri-Bold"
                          >책 바로가기</v-btn
                        >
                        <v-btn
                          v-show="isYou"
                          @click="like(book.id, idx)"
                          text
                          outlined
                          color="white"
                          class=""
                          style="font-family: HangeulNuri-Bold"
                          >좋아요 취소</v-btn
                        >
                      </v-row>
                    </div>
                  </div>
                </v-col>
              </v-row>
              <v-row v-else>
                <v-col>
                  <h4
                    class="text-center mt-1"
                    style="font-family: HangeulNuri-Bold"
                  >
                    좋아요 한 책이 없습니다.
                  </h4>
                </v-col>
              </v-row>
              <v-pagination
                v-if="alllikeBooks != '좋아요한 책이 없습니다.'"
                color="#009688"
                class="main-font"
                v-model="likeBookPage"
                :length="likeBookPages"
                circle
              ></v-pagination>
            </v-container>
          </v-tab-item>
          <!-- 작성한 리뷰 -->
          <v-tab-item>
            <v-container fluid class="pb-0">
              <v-row v-if="allReviews != '작성한 review 가 없습니다.'">
                <v-col
                  v-for="review in myReviews"
                  :key="review.id"
                  cols="3"
                  lg="3"
                  sm="6"
                  xs="6"
                  class="pt-0"
                >
                  <div class="card cursor">
                    <v-img
                      v-if="review.book_img_url"
                      class="imgBx bookimage"
                      :src="review.book_img_url"
                    ></v-img>
                    <v-img
                      v-else
                      class="imgBx bookimage"
                      src="@/assets/img/no-image.jpg"
                    ></v-img>

                    <div class="details">
                      <div v-if="review.title">
                        <h6
                          v-show="review.title.length > 10"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ review.title.slice(0, 10) }}...
                        </h6>
                        <h6
                          v-show="review.title.length <= 10"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ review.title }}
                        </h6>
                      </div>
                      <div v-else>
                        <h6 style="font-family: HangeulNuri-Bold">
                          제목이 없는 책입니다.
                        </h6>
                      </div>
                      <div v-if="review.content" style="height: 100px">
                        <small
                          v-show="review.content.length > 60"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ review.content.slice(0, 60) }}...
                        </small>
                        <small
                          v-show="review.content.length <= 60"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ review.content }}
                        </small>
                      </div>
                      <div v-else style="height: 100px">
                        <small style="font-family: HangeulNuri-Bold"
                          >리뷰 내용이 없습니다.</small
                        >
                      </div>
                      <v-row class="mt-5 d-flex justify-content-center">
                        <v-btn
                          @click="goToReviewDetail(review.id)"
                          text
                          outlined
                          color="white"
                          class="mt-3"
                          style="font-family: HangeulNuri-Bold"
                          >리뷰 바로가기</v-btn
                        >
                      </v-row>
                    </div>
                  </div>
                </v-col>
              </v-row>
              <v-row v-else>
                <v-col>
                  <h4
                    class="text-center mt-5"
                    style="font-family: HangeulNuri-Bold"
                  >
                    작성한 리뷰가 없습니다.
                  </h4>
                </v-col>
              </v-row>
              <v-pagination
                v-if="allReviews != '작성한 review 가 없습니다.'"
                class="main-font"
                color="#009688"
                v-model="reviewPage"
                :length="reviewPages"
                circle
              ></v-pagination>
            </v-container>
          </v-tab-item>
          <!-- 작성한 문장 -->
          <v-tab-item>
            <v-container fluid>
              <v-row style="font-family: HangeulNuri-Bold; font-size: large">
                <v-col cols="2" class="text-center">책 제목</v-col>
                <v-col cols="6" class="text-center">글귀내용</v-col>
                <v-col v-show="isYou" cols="2" class="text-center px-0"
                  >글귀 삭제</v-col
                >
                <v-col cols="2" class="text-center px-0">책 바로가기</v-col>
              </v-row>
              <v-divider></v-divider>
              <div v-if="allPhrases != '작성한 phrase 가 없습니다.'">
                <v-row
                  v-for="phrase in myPhrases"
                  :key="phrase.id"
                  style="font-family: HangeulNuri-Bold"
                >
                  <v-col cols="2" class="text-center pt-5">{{
                    phrase.book_title
                  }}</v-col>
                  <v-col cols="6" class="text-center">{{
                    phrase.content
                  }}</v-col>
                  <v-col v-show="isYou" cols="2" class="text-center px-0">
                    <v-btn
                      text
                      @click="deletePhrase(phrase.id)"
                      style="font-size: medium; color: gray"
                      ><i class="fas fa-trash"></i></v-btn
                  ></v-col>
                  <v-col cols="2" class="text-center px-0">
                    <v-btn text>
                      <v-icon
                        medium
                        @click="goToBookDetail(phrase.book)"
                        uk-tooltip="책 바로가기"
                      >
                        mdi-link-variant
                      </v-icon></v-btn
                    ></v-col
                  >
                </v-row>
                <div class="text-center">
                  <v-pagination
                    class="main-font"
                    color="#009688"
                    v-model="phrasePage"
                    :length="phrasePages"
                    circle
                  ></v-pagination>
                </div>
              </div>
              <div v-else>
                <v-row>
                  <v-col>
                    <h4
                      class="text-center mt-5"
                      style="font-family: HangeulNuri-Bold"
                    >
                      작성한 문장이 없습니다.
                    </h4>
                  </v-col>
                </v-row>
              </div>
            </v-container>
          </v-tab-item>
        </v-tabs>
      </v-card>

      <!-- 북릿지 활동 -->

      <v-card height="100%" id="bookActivity" class="scrollme3">
        <v-system-bar color="#004D40"> </v-system-bar>
        <v-card-text>
          <v-row class="d-flex justify-content-center">
            <h2 class="my-5" style="font-family: HangeulNuri-Bold">
              📝{{ name }}님의 북릿지활동
            </h2>
          </v-row>
        </v-card-text>
        <v-tabs background-color="white" color="#009688" centered>
          <v-tab style="font-family: HangeulNuri-Bold">좋아요한 리뷰</v-tab>
          <v-tab style="font-family: HangeulNuri-Bold">작성한 댓글</v-tab>
          <!-- 좋아요한 리뷰 -->
          <v-tab-item>
            <v-container fluid class="pb-0">
              <v-row v-if="alllikeReviews != '좋아요한 review 가 없습니다.'">
                <v-col
                  v-for="(review, idx) in likeReviews"
                  :key="idx"
                  cols="3"
                  lg="3"
                  sm="6"
                  xs="6"
                  class="pt-0"
                >
                  <div class="card cursor">
                    <v-img
                      v-if="review.book_img_url"
                      class="imgBx bookimage"
                      :src="review.book_img_url"
                    ></v-img>
                    <v-img
                      v-else
                      class="imgBx bookimage"
                      src="@/assets/img/no-image.jpg"
                    ></v-img>

                    <div class="details">
                      <div v-if="review.title">
                        <h6
                          v-show="review.title.length > 10"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ review.title.slice(0, 10) }}...
                        </h6>
                        <h6
                          v-show="review.title.length <= 10"
                          style="font-family: HangeulNuri-Bold"
                        >
                          {{ review.title }}
                        </h6>
                      </div>
                      <div v-else>
                        <h6 style="font-family: HangeulNuri-Bold">
                          제목이 없는 책입니다.
                        </h6>
                      </div>
                      <div v-if="review.content" style="height: 100px">
                        <small
                          v-show="review.content.length > 60"
                          style="
                            font-family: HangeulNuri-Bold;
                            text-align: center;
                          "
                        >
                          {{ review.content.slice(0, 60) }}...
                        </small>
                        <small
                          v-show="review.content.length <= 60"
                          style="
                            font-family: HangeulNuri-Bold;
                            text-align: center;
                          "
                        >
                          {{ review.content }}
                        </small>
                      </div>
                      <div v-else style="height: 100px">
                        <small style="font-family: HangeulNuri-Bold"
                          >리뷰 내용이 없습니다.</small
                        >
                      </div>
                      <v-row class="mt-5 d-flex justify-content-center">
                        <v-btn
                          @click="goToReviewDetail(review.id)"
                          text
                          outlined
                          color="white"
                          class="mt-3"
                          style="font-family: HangeulNuri-Bold"
                          >리뷰 바로가기</v-btn
                        >
                        <v-btn
                          v-show="isYou"
                          @click="reviewLike(review, idx)"
                          text
                          outlined
                          color="white"
                          class=""
                          style="font-family: HangeulNuri-Bold"
                          >좋아요 취소</v-btn
                        >
                      </v-row>
                    </div>
                  </div>
                </v-col>
              </v-row>
              <v-row v-else>
                <v-col>
                  <h4
                    class="text-center mt-5"
                    style="font-family: HangeulNuri-Bold"
                  >
                    좋아요한 리뷰가 없습니다.
                  </h4>
                </v-col>
              </v-row>
              <v-pagination
                v-if="alllikeReviews != '좋아요한 review 가 없습니다.'"
                class="main-font"
                color="#009688"
                v-model="likeReviewPage"
                :length="likeReviewPages"
                circle
              ></v-pagination>
            </v-container>
          </v-tab-item>
          <!-- 작성한 댓글 -->
          <v-tab-item>
            <v-container fluid>
              <v-row style="font-family: HangeulNuri-Bold">
                <v-col cols="6" class="text-center"> 댓글 내용 </v-col>
                <v-col cols="2" class="text-center"> 작성 시간 </v-col>
                <v-col v-show="isYou" cols="2" class="text-center">
                  댓글 삭제</v-col
                >
                <v-col cols="2" class="text-center">리뷰 바로가기</v-col>
              </v-row>
              <hr />
              <div v-if="allComments != '작성한 comment 가 없습니다.'">
                <v-row
                  v-for="com in myComments"
                  :key="com.id"
                  style="font-family: HangeulNuri-Bold"
                >
                  <v-col cols="6" class="text-center">{{ com.content }}</v-col>
                  <v-col cols="2" class="text-center">{{
                    com.created_at.slice(0, 10) +
                    " " +
                    com.created_at.slice(11, 16)
                  }}</v-col>
                  <v-col v-show="isYou" cols="2" class="text-center">
                    <v-btn
                      text
                      @click="deleteComment(com)"
                      style="font-size: medium; color: gray"
                      ><i class="fas fa-trash"></i></v-btn
                  ></v-col>
                  <v-col cols="2" class="text-center">
                    <v-icon
                      medium
                      @click="goToReviewDetail(com.review)"
                      uk-tooltip="리뷰 바로가기"
                    >
                      mdi-link-variant
                    </v-icon>
                  </v-col>
                </v-row>
                <div class="text-center">
                  <v-pagination
                    class="main-font"
                    color="#009688"
                    v-model="commentPage"
                    :length="commentPages"
                    circle
                  ></v-pagination>
                </div>
              </div>
              <div v-else>
                <v-row>
                  <v-col>
                    <h4
                      class="text-center mt-5"
                      style="font-family: HangeulNuri-Bold"
                    >
                      작성한 댓글이 없습니다.
                    </h4>
                  </v-col>
                </v-row>
              </div>
            </v-container>
          </v-tab-item>
        </v-tabs>
      </v-card>

      <!-- 독서 성향 -->

      <v-card height="100%" id="bookTendency" class="scrollme4">
        <v-system-bar color="#004D40"> </v-system-bar>
        <v-card-text>
          <MyChart
            :name="name"
            :radar="radar"
            :line="line"
            :info="info"
            v-if="temp"
          />
        </v-card-text>
      </v-card>

      <!-- 리모콘 -->
      <v-speed-dial
        v-model="fab"
        direction="top"
        transition="slide-y-reverse-transition"
        class="temp_spy"
      >
        <template v-slot:activator>
          <v-btn v-model="fab" dark fab color="blue-grey">
            <v-icon v-if="fab">mdi-close</v-icon>
            <v-icon v-else>mdi-view-grid</v-icon>
          </v-btn>
        </template>
        <v-btn
          v-scroll="onScroll"
          text
          style="
            font-family: HangeulNuri-Bold;
            font-size: medium;
            background-color: #f5f5f5;
          "
          @click="toTop"
        >
          <h5>⬆</h5>
          위로가기
        </v-btn>
        <v-btn
          text
          :class="{ active: isActive4 }"
          @click="goToSomewhere('bookTendency')"
          style="
            font-family: HangeulNuri-Bold;
            font-size: medium;
            background-color: #f5f5f5;
          "
        >
          👨‍💻독서성향</v-btn
        >
        <v-btn
          text
          :class="{ active: isActive3 }"
          @click="goToSomewhere('bookActivity')"
          style="
            font-family: HangeulNuri-Bold;
            font-size: medium;
            background-color: #f5f5f5;
          "
          >📝활동내역</v-btn
        >
        <v-btn
          text
          :class="{ active: isActive2 }"
          @click="goToSomewhere('bookShelf')"
          style="
            font-family: HangeulNuri-Bold;
            font-size: medium;
            background-color: #f5f5f5;
          "
        >
          📚나의서재</v-btn
        >
        <v-btn
          text
          :class="{ active: isActive1 }"
          @click="goToSomewhere('bookLog')"
          style="
            font-family: HangeulNuri-Bold;
            font-size: medium;
            background-color: #f5f5f5;
          "
          >📅독서기록</v-btn
        >
      </v-speed-dial>
    </v-container>
  </div>
</template>

<script>
import swal from "sweetalert";
import axios from "axios";
import VueCookies from "vue-cookies";
import MyChart from "./MyChart.vue";

// import Calendar from "./Calendar.vue";

export default {
  name: "Profile",
  components: { MyChart },

  beforeRouteEnter(to, from, next) {
    if (!VueCookies.get("jwt_token")) {
      next("/");
      // swal("잘못된 접근입니다.1");
    } else {
      next();
    }
  },
  computed: {
    SDateMax() {
      return new Date().toISOString().split("T")[0];
    },
    EDateMin() {
      // 컨퍼런스를 생성하는 경우 시작일 제한
      if (this.Sdate == "") {
        return new Date().toISOString().split("T")[0];
      } else {
        return this.Sdate;
      }
    },
    EDateMax() {
      return new Date().toISOString().split("T")[0];
    },
  },
  mounted() {
    this.arrayEvents = [...Array(6)].map(() => {
      const day = Math.floor(Math.random() * 30);
      const d = new Date();
      d.setDate(day);
      return d.toISOString().substr(0, 10);
    });
  },

  data() {
    return {
      isUpdate: false,
      updateTarget: "",
      temp: false,
      radar: [],
      line: [],
      info: [],
      page: 0,
      // 좋아요한 책
      likeBookPage: 1,
      likeBookPages: 1,
      // 작성한 리뷰
      reviewPage: 1,
      reviewPages: 1,
      // 좋아요한 리뷰
      likeReviewPage: 1,
      likeReviewPages: 1,

      //
      commentPage: 1,
      commentPages: 1,
      phrasePage: 1,
      phrasePages: 1,
      todayBlueBook: [],
      todayRedBook: [],

      isActive1: false,
      isActive2: false,
      isActive3: false,
      isActive4: false,

      pickedBook: null,
      isSelected: false,
      dialog: false,
      dialogDelete: false,

      myReviews: [],
      allReviews: [],

      myPhrases: [],
      allPhrases: [],

      myComments: [],
      allComments: [],

      likeBooks: [],
      alllikeBooks: [],

      likeReviews: [],
      alllikeReviews: [],

      myCalendar: null,
      autoBooks: null,
      searchWord: null,
      dailyBook: true,
      rules: {
        startDate(val) {
          if (val) return true;
          else return "시작날짜를 선택해주세요.";
        },
      },
      valid: false,
      startDates: [],
      endDates: [],
      arrayEvents: null,
      date: new Date().toISOString().substr(0, 10),
      Sdate: "",
      Edate: "",

      validName: true,
      nameRules: [
        (v) => !!v || "이름은 필수값입니다.",
        (v) => (v && v.length <= 10) || "이름은 10자 이내로 입력해주세요.",
      ],
      dialgotest: false,
      isLogin: true,

      visible: false,
      index: 0,

      show1: false,
      show2: false,

      rulesPw: [
        (v) => !!v || "비밀번호는 필수값입니다.",
        (v) => (v && v.length >= 8) || "비밀번호는 8자 이상으로 입력해주세요.",
      ],

      genders: ["남자", "여자"],
      afterProfileImg: null,
      profileImgUrl: null,

      // 개인정보
      userPk: "", // 프로필 주인
      name: "", // 닉네임
      newName: "", // 새로운 닉네임

      email: null,

      birth: null,
      newBirth: null,
      menu: false,
      menuStart: false,
      menuEnd: false,

      nowPassword: null,
      password: null, // 기존비밀번호
      newPassword1: "", // 새로운 비밀번호1
      newPassword2: "", // 새로운 비밀번호2

      gender: null,
      newGender: null,

      hide: false,
      longitude: null,
      latitude: null,

      address: null,
      newAddress: null,

      social: null,

      profileImg: null,

      // dialog 모음
      dialogCalendar: false,
      dialogPI: false,
      dialogBirth: false,
      // 프로필 수정시 비밀번호 물어보는 dialog
      dialogPw: false,
      // 개인보안 dialog
      dialogSecurityAccount: false,
      // 비밀번호 수정 dialog
      dialogChangePw: false,
      // 회원탈퇴 dialog
      dialogDeleteAccount: false,
      // 본인일치여부
      isYou: false,

      // 수정 여부
      updateNow: false,
      updatePwNow: false,

      // 스크롤
      fab: false,

      // 탭
      tab: null,

      // 기본정보 값
      isLoading: false,
      nextItem: 1,
      // pagination
      perPage: 5,
      currentPage: 1,
      start: 0,
      end: 5,

      //댓글
      comments: [],
    };
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  created() {
    this.$vuetify.goTo(0);

    window.addEventListener("scroll", this.handleScroll);

    // 다 읽은 책
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/accounts/get_finish_list/`, {
        params: {
          user_pk: VueCookies.get("user_pk"),
        },
      })
      .then(() => {});

    // 소셜 회원가입 미완료할 경우
    if (VueCookies.get("user_gender") == 2) {
      swal("잘못된 접근입니다.", "회원가입이 완료되지 않았습니다.");
      this.$router.push("/signup");
    }

    // this.isLoading = true;
    this.isLogin = VueCookies.get("jwt_token") ? true : false;
    this.userPk = this.$route.params.pk; // userPk
    // 본인 일치치여부 확인
    if (VueCookies.get("user_pk") == this.userPk) {
      this.isYou = true;
    }

    // 프로필 정보 가져오기
    axios
      .get(
        `${process.env.VUE_APP_SERVER_URL}/accounts/profile/${this.$route.params.pk}/`,
        {
          headers: {
            Authorization: VueCookies.get("jwt_token"),
          },
        }
      )
      .then((res) => {
        // console.log("회원정보 가져오기");
        // console.log(res);
        this.name = res.data.name;
      });
    // .catch((err) => {
    //   console.log(err);
    // });

    // 좋아요한 책 불러오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/accounts/profile/like/`, {
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        // console.log("좋아요한 책");
        // console.log(res);
        this.likeBooks = res.data.result.slice(0, 8);
        this.alllikeBooks = res.data.result;
        this.likeBookPages = parseInt(this.alllikeBooks.length / 8) + 1;
      });
    // .catch((err) => {
    //   console.log(err);
    // });

    // 글귀 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/accounts/profile/phrase/`, {
        params: {
          user_pk: this.userPk,
        },
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        // console.log("글귀 가져오기");
        // console.log(res);
        this.myPhrases = res.data.result.slice(0, 5);
        this.allPhrases = res.data.result;
        this.phrasePages = parseInt(this.allPhrases.length / 5) + 1;
      });
    // .catch((err) => {
    //   console.log(err);
    // });

    // 리뷰 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/accounts/profile/review/`, {
        params: {
          user_pk: this.userPk,
        },
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        // console.log("작성한 리뷰");
        // console.log(res);
        this.myReviews = res.data.result.slice(0, 8);

        this.allReviews = res.data.result;
        this.reviewPages = parseInt(this.allReviews.length / 8) + 1;
      });
    // .catch((err) => {
    //   console.log(err);
    // });

    // 좋아요 한 리뷰 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/accounts/profile/like_review/`, {
        params: {
          user_pk: this.userPk,
        },
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        // console.log("좋아요한 리뷰");
        // console.log(res);
        this.likeReviews = res.data.result.slice(0, 8);
        this.alllikeReviews = res.data.result;
        this.likeReviewPages = parseInt(this.alllikeReviews.length / 8) + 1;
      });
    // .catch((err) => {
    //   console.log(err);
    // });

    // 댓글 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/accounts/profile/comment/`, {
        params: {
          user_pk: this.$route.params.pk,
        },
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        // console.log("작성한 댓글");
        // console.log(res.data.result);
        this.myComments = res.data.result.slice(0, 5);
        this.allComments = res.data.result;
        this.commentPages = parseInt(this.allComments.length / 5) + 1;
      });
    // .catch((err) => {
    //   console.log(err);
    // });
    // 캘린더 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/accounts/calendar/`, {
        params: { user_pk: this.userPk },
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        // console.log("캘린더 가져오기");
        // console.log(res);
        this.myCalendar = res.data.result;

        let today = new Date();
        let year = today.getFullYear().toString(); // 년도
        let month = (today.getMonth() + 1).toString(); // 월
        let day = today.getDate().toString(); // 날짜
        if (month.length == 1) {
          month = "0" + month;
        }
        if (day.length == 1) {
          day = "0" + day;
        }
        this.getCalendar(year + "-" + month + "-" + day);

        for (let idx = 0; idx < this.myCalendar.length; idx++) {
          if (this.myCalendar[idx]["calendar"]["end_date"] == null) {
            this.startDates.push(
              this.myCalendar[idx]["calendar"]["start_date"]
            );
          } else {
            this.endDates.push(this.myCalendar[idx]["calendar"]["end_date"]);
          }
        }
      });
    // .catch((err) => {
    //   console.log(err);
    // });
    // 차트 데이터 가져오기
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/accounts/profile/chart/`, {
        params: { user_pk: this.userPk },
        headers: { Authorization: VueCookies.get("jwt_token") },
      })
      .then((res) => {
        this.info = res.data.radar_info;
        this.radar = res.data.radar.slice(1, 10);
        this.line = res.data.line;
      });
    // .catch((err) => {
    //   console.log(err);
    // });
    setTimeout(() => {
      this.temp = true;
    }, 2000);
  },

  watch: {
    menu(val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = "YEAR"));
    },
    date(date) {
      this.getCalendar(date);
    },
    commentPage(event) {
      this.myComments = this.allComments.slice((event - 1) * 5, event * 5);
    },
    phrasePage(event) {
      this.myPhrases = this.allPhrases.slice((event - 1) * 5, event * 5);
    },
    likeBookPage(event) {
      this.likeBooks = this.alllikeBooks.slice((event - 1) * 8, event * 8);
    },
    reviewPage(event) {
      this.myReviews = this.allReviews.slice((event - 1) * 8, event * 8);
    },
    likeReviewPage(event) {
      this.likeReviews = this.alllikeReviews.slice((event - 1) * 8, event * 8);
    },
  },

  methods: {
    beforeUpdate(book) {
      this.updateTarget = book;
      this.isUpdate = true;
      this.dialogCalendar = true;
      this.pickedBook = book.book;
      this.isSelected = true;
      this.Sdate = book.calendar.start_date;
      this.Edate = book.calendar.end_date;

      // console.log(book);
    },
    // 글귀 삭제
    deletePhrase(pk) {
      axios
        .delete(`${process.env.VUE_APP_SERVER_URL}/reviews/phrase/`, {
          params: { phrase_pk: pk },
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then(() => {
          swal("글귀가 삭제되었습니다.");

          axios
            .get(`${process.env.VUE_APP_SERVER_URL}/accounts/profile/phrase/`, {
              params: {
                user_pk: this.userPk,
              },
              headers: { Authorization: VueCookies.get("jwt_token") },
            })
            .then((res) => {
              this.phrasePage = 1;
              this.myPhrases = res.data.result.slice(0, 5);
              this.allPhrases = res.data.result;
              this.phrasePages = parseInt(this.allPhrases.length / 5) + 1;
            });
        });
    },
    deleteComment(com) {
      // console.log(com);
      axios
        .delete(`${process.env.VUE_APP_SERVER_URL}/reviews/comment/`, {
          params: {
            comment_pk: com.id,
            review_pk: com.review,
          },
          headers: {
            Authorization: VueCookies.get("jwt_token"),
          },
        })
        .then((res) => {
          this.commentPage = 1;
          this.myComments = res.data.result.slice(0, 5);
          this.allComments = res.data.result;
          this.commentPages = parseInt(this.allComments.length / 5) + 1;
          swal("댓글이 삭제되었습니다.");
        });
    },

    goToSomewhere(item) {
      window.scrollTo(0, document.getElementById(item).offsetTop);
    },
    handleScroll() {
      const els = document.querySelectorAll(".scrollme1");

      els.forEach((el) => {
        const elTop = el.getBoundingClientRect().top;
        const elBottom = el.getBoundingClientRect().bottom;
        if (elTop >= 0 || elBottom <= 0) {
          this.isActive1 = false;
        }
        if (elTop <= 0 && elBottom >= 0) {
          this.isActive1 = true;
        }
      });
      const els2 = document.querySelectorAll(".scrollme2");
      els2.forEach((el2) => {
        const elTop2 = el2.getBoundingClientRect().top;
        const elBottom2 = el2.getBoundingClientRect().bottom;
        if (elTop2 >= 0 || elBottom2 <= 0) {
          this.isActive2 = false;
        }
        if (elTop2 <= 0 && elBottom2 >= 0) {
          this.isActive2 = true;
        }
      });
      const els3 = document.querySelectorAll(".scrollme3");
      els3.forEach((el3) => {
        const elTop3 = el3.getBoundingClientRect().top;
        const elBottom3 = el3.getBoundingClientRect().bottom;
        if (elTop3 >= 0 || elBottom3 <= 0) {
          this.isActive3 = false;
        }
        if (elTop3 <= 0 && elBottom3 >= 0) {
          this.isActive3 = true;
        }
      });
      const els4 = document.querySelectorAll(".scrollme4");
      els4.forEach((el4) => {
        const elTop4 = el4.getBoundingClientRect().top;
        const elBottom4 = el4.getBoundingClientRect().bottom;
        if (elTop4 >= 0 || elBottom4 <= 0) {
          this.isActive4 = false;
        }
        if (elTop4 <= 0 && elBottom4 >= 0) {
          this.isActive4 = true;
        }
      });
      const els5 = document.querySelectorAll(".scrollme5");
      els5.forEach((el5) => {
        const elTop5 = el5.getBoundingClientRect().top;
        const elBottom5 = el5.getBoundingClientRect().bottom;
        if (elTop5 >= 0 || elBottom5 <= 0) {
          this.isActive5 = false;
        }
        if (elTop5 <= 0 && elBottom5 >= 0) {
          this.isActive5 = true;
        }
      });
    },

    // 책 선택
    selectBook(book) {
      this.isSelected = true;
      this.pickedBook = book;
    },
    // 책 선택 취소
    cancelSelect() {
      (this.isSelected = false), (this.pickedBook = null);
    },

    cancelCalendar() {
      this.dialogCalendar = false;
      this.Sdate = "";
      this.Edate = "";
      this.isSelected = false;
      this.pickedBook = null;
      this.isUpdate = false;
    },
    // 리뷰 좋아요 취소
    reviewLike(review, idx) {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/reviews/like/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            review_pk: review.id,
          },
        })
        .then(() => {
          // console.log("좋아요 결과");
          // console.log(res);
          review.review_like_state = !review.review_like_state;

          this.alllikeReviews.splice(8 * (this.likeReviewPage - 1) + idx, 1);
          this.likeReviews = this.alllikeReviews.slice(0, 8);
          this.likeReviewPage = 1;
          this.likeReviewPages = parseInt(this.alllikeReviews.length / 8) + 1;
          swal("좋아요가 취소되었습니다.");
        });
    },
    // 책 좋아요 취소
    like(pk, idx) {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/like/`, {
          params: {
            user_pk: VueCookies.get("user_pk"),
            book_pk: pk,
          },
        })
        .then(() => {
          swal("좋아요가 취소되었습니다.");
          // sessionStorage.clear();

          this.alllikeBooks.splice(8 * (this.likeBookPage - 1) + idx, 1);

          this.likeBooks = this.alllikeBooks.slice(0, 8);
          this.likeBookPage = 1;

          this.likeBookPages = parseInt(this.alllikeBooks.length / 8) + 1;
        });
    },
    goToBookDetail(id) {
      this.$router.push(`/bookdetail/${id}`);
    },
    goToReviewDetail(id) {
      this.$router.push(`/reviewdetail/${id}`);
    },
    bookSearch() {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/books/book_auto_search/`, {
          params: {
            search_word: this.searchWord,
          },
        })
        .then((res) => {
          this.autoBooks = res.data.result;
        });
    },

    // 캘린더 가져오기
    getCalendar(date) {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/calendar/`, {
          params: {
            user_pk: this.userPk,
            date: date,
          },
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then((res) => {
          // console.log("해당 캘린더 가져오기");
          // console.log(res);
          this.todayBlueBook = res.data.red;
          this.todayRedBook = res.data.yellow;
        });
    },

    // 캘린더 추가
    createCalendar() {
      axios
        .put(
          `${process.env.VUE_APP_SERVER_URL}/accounts/calendar/`,
          {
            start_date: this.Sdate,
            end_date: this.Edate,
            book_pk: this.pickedBook.id,
          },
          {
            headers: { Authorization: VueCookies.get("jwt_token") },
          }
        )
        .then(() => {
          swal("도서가 추가되었습니다!", {
            button: false,
          });
          this.dialogCalendar = false;
          this.isSelected = false;
          this.pickedBook = null;
          this.Sdate = null;
          this.Edate = null;
          // console.log("캘린더 생성");
          // console.log(res);
          this.$router.go();
        });
    },

    // 캘린더 수정
    updateCalendar() {
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/accounts/calendar/`,
          {
            book_pk: this.updateTarget.book.id,
            calendar_pk: this.updateTarget.calendar.id,
            start_date: this.Sdate,
            end_date: this.Edate,
          },
          {
            headers: { Authorization: VueCookies.get("jwt_token") },
          }
        )
        .then(() => {
          swal("도서가 수정되었습니다!", {
            button: false,
          });
          // console.log("수정 후...");
          // console.log(res);
          this.cancelCalendar();
          this.$router.go();
        })
        // .catch((err) => {
        //   console.log(err);
        // });
    },
    // 캘린더 삭제
    deleteCalendar(pk) {
      axios
        .delete(`${process.env.VUE_APP_SERVER_URL}/accounts/calendar/`, {
          params: { calendar_pk: pk },
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then(() => {
          // console.log("캘린더 삭제 결과");
          // console.log(res);
          this.$router.go();
        });
    },

    calendarEvents(date) {
      // console.log(date);
      this.myCalendar;
      for (var i = 0; i < this.startDates.length; i++) {
        if (this.startDates[i] == date) {
          for (let x = 0; x < this.endDates.length; x++) {
            if (this.endDates[x] == date) {
              return ["red", "blue"];
            }
          }
          return ["red"];
        }
      }
      for (var j = 0; j < this.endDates.length; j++) {
        if (this.endDates[j] == date) {
          return ["blue"];
        }
      }
      return false;
    },
    save(date) {
      this.$refs.menu.save(date);
    },
    showLightbox(index) {
      this.index = index;
      this.visible = true;
    },

    // 모달 닫는 부분
    closeDialog() {
      this.dialogPw = false;
      this.dialogChangePw = false;
      this.password = "";
      this.newPassword1 = "";
      this.newPassword2 = "";
    },

    // 스크롤(Top)
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },

    // 최상단으로 이동하기
    toTop() {
      this.$vuetify.goTo(0);
    },
  },
};
</script>

<style scoped>
.cursor {
  cursor: pointer;
}
.main-font {
  font-family: "HangeulNuri-Bold";
}

.card {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 300px;
  background: #262626;
  overflow: hidden;
}

.card .details {
  position: absolute;
  box-sizing: border-box;
  transition: 0.5s;
}

.card .details {
  background: #262626;
  top: 0;
  left: 100%;
  padding: 30px 20px;
}
.card:hover .details {
  top: 0;
  left: 0%;
}
.card .details h6 {
  color: #fff;
  text-align: center;
  padding: 0 0 10px;
  border-bottom: 2px solid #fff;
}
.card .details small {
  color: #fff;
}

/*  */

.text-white {
  color: white;
}
.bookimage {
  width: 200px;
  height: 300px;
  margin: 0px;
}

.v-responsive__content {
  margin-left: 0px;
}

/* .container {
  z-index: 1;
  perspective: 3000px;
} */

.container .book {
  position: relative;
  display: block;
  width: 400px;
  height: 550px;
  margin: 5% auto;
  border-radius: 2px 4px 4px 2px;
  background: linear-gradient(45deg, #dad5dc 0%, #f2ebf4 100%);
  font-family: acumin-pro, sans-serif;
  -webkit-box-shadow: 13px 13px 8px 0px rgba(151, 146, 153, 0.6);
  -moz-box-shadow: 13px 13px 8px 0px rgba(151, 146, 153, 0.6);
  box-shadow: 13px 13px 8px 0px rgba(151, 146, 153, 0.6);
  font-weight: 400;
  color: #2b2b2b;
  -webkit-transform-style: preserve-3d;
  -moz-transform-style: preserve-3d;
  transform-style: preserve-3d;
  -webkit-transition: -webkit-transform 0.5s;
  -moz-transition: -moz-transform 0.5s;
  transition: transform 0.5s;
}

.container .book:hover {
  -webkit-transform: rotate3d(0, 1, 0, 35deg);
  -moz-transform: rotate3d(0, 1, 0, 35deg);
  transform: rotate3d(0, 1, 0, 35deg);
}

.container .book > div,
.container .front > div {
  display: block;
  position: absolute;
}

.container .front {
  -webkit-transform-style: preserve-3d;
  -moz-transform-style: preserve-3d;
  transform-style: preserve-3d;
  -webkit-transform-origin: 0% 50%;
  -moz-transform-origin: 0% 50%;
  transform-origin: 0% 50%;
  -webkit-transition: -webkit-transform 0.5s;
  -moz-transition: -moz-transform 0.5s;
  transition: transform 0.5s;
  -webkit-transform: translate3d(0, 0, 20px);
  -moz-transform: translate3d(0, 0, 20px);
  transform: translate3d(0, 0, 20px);
  z-index: 10;
}

.container .front > div {
  width: 400px;
  height: 550px;
}

.container .left-side {
  width: 40px;
  left: -20px;
  height: 550px;
  background-color: rgba(232, 229, 234);
  -webkit-transform: rotate3d(0, 1, 0, -90deg);
  -moz-transform: rotate3d(0, 1, 0, -90deg);
  transform: rotate3d(0, 1, 0, -90deg);
}

#eye-right {
  padding-left: 185px;
}

.author {
  font-weight: 400;
  position: absolute;
  top: 475px;
  left: 50px;
  opacity: 0.8;
}

.container .front > div {
  border-radius: 0 3px 3px 0;
  box-shadow: inset 4px 0 10px rgba(0, 0, 0, 0.1);
}

.container .front:after {
  content: "";
  position: absolute;
  top: 1px;
  bottom: 1px;
  left: -1px;
  width: 1px;
}

.container .cover:after {
  content: "";
  position: absolute;
  top: 0;
  left: 10px;
  bottom: 0;
  width: 3px;
  box-shadow: 1px 0 3px rgba(255, 255, 255, 0.1);
}

.cover {
  background: linear-gradient(45deg, #dad5dc 0%, #f2ebf4 100%);
}

.left-side h6 span:first-child {
  padding-right: 20px;
}

/* 내가 작성한 CSS */
.vertical {
  vertical-align: middle;
}

.v-tabs-slider {
  background-color: white;
}
.address-btn {
  font-size: 15px;
  width: 50;
  background-color: white;

  color: green;
  padding: 6px 14px;

  margin: 4px 2px;
  cursor: pointer;
}
.address-btn:hover {
  opacity: 0.9;
  border: none;
  border-radius: 5px;
  box-shadow: 0.5px 0.5px 0.5px 0.5px #bdbdbd;
}

.text-blue {
  color: #42a5f5;
}

@font-face {
  font-family: "HangeulNuri-Bold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
  font-size: x-large;
}

.v-tab.v-tab--active {
  color: #4db6ac !important;
}

.v-system-bar.theme--light {
  margin-top: 5%;
}

@font-face {
  font-family: "TmonMonsori";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/TmonMonsori.woff")
    format("woff");
  font-weight: lighter;
  font-style: normal;
}
@font-face {
  font-family: "InfinitySans-RegularA1";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/InfinitySans-RegularA1.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}

.temp_spy {
  display: flex;
  flex-direction: column;
  position: fixed;
  right: 2%;
  bottom: 5%;
  font-size: 1em;
}
.active {
  font-size: 2em;
}
.col.col-3 {
  padding: 4%;
}
.do {
  font-family: "Do Hyeon", sans-serif;
}
.v-card__title.main-color.justify-content-center {
  background-color: #4db6ac;
}
.details {
  width: 200px;
  height: 300px;
}
.text-center.col.col-3 {
  padding: 12px;
}
</style>
