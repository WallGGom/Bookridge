<template>
  <div>
    <mdb-container>
      <h2 class="h1-responsive font-weight-bold text-center my-5">
        BOOKRIDGE LIBRARY
      </h2>
      <h6
        class="text-center w-responsive mx-auto mb-5 do"
        style="font-size: large"
      >
        {{ name }}님을 위해 다양한 추천방식으로 도서 추천 서비스를 제공합니다.
      </h6>
      <br />
      <div v-if="!isLoading">
        <v-system-bar dark color="#34495e" class="mb-5">
          <v-spacer></v-spacer>
        </v-system-bar>
        <mdb-row>
          <mdb-col v-if="algorithm5.length != 0" lg="8">
            <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
              <div
                class="uk-position-relative uk-visible-toggle uk-light"
                tabindex="-1"
                uk-slider
              >
                <ul
                  class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
                >
                  <li v-for="algo of algorithm5" :item="algo" :key="algo.id">
                    <mdb-view hover class="zoom">
                      <img
                        v-if="algo.img_url"
                        :src="algo.img_url"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <img
                        v-else
                        src="@/assets/img/no-image.jpg"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <mdb-mask flex-center waves overlay="black-strong">
                        <mdb-btn
                          v-if="algo.title.length > 50"
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title.slice(0, 50) }} ... 자세히
                          보기</mdb-btn
                        >
                        <mdb-btn
                          v-else
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title }} - 자세히 보기</mdb-btn
                        >
                      </mdb-mask>
                    </mdb-view>

                    <div class="uk-position-center uk-panel"></div>
                  </li>
                </ul>

                <a
                  class="uk-position-center-left uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-previous
                  uk-slider-item="previous"
                ></a>
                <a
                  class="uk-position-center-right uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-next
                  uk-slider-item="next"
                ></a>
              </div>
              <a>
                <mdb-mask overlay="white-slight" waves />
              </a>
            </div>
          </mdb-col>
          <mdb-col v-else lg="8" class="no-data1 my-auto">
            <h4 style="font-family: HangeulNuri-Bold">
              선택한 장르가 없습니다.
            </h4>
            <p style="font-family: HangeulNuri-Bold">
              프로필에서 장르를 선택하시면 해당 추천이 활성화됩니다.
            </p>
          </mdb-col>
          <mdb-col
            lg="4"
            style="margin-top: 3%"
            class="text-right align-items-end"
          >
            <h6
              class="font-weight-bold mb-3"
              style="font-family: 'HangeulNuri-Bold'"
            >
              Genre
            </h6>

            <h3
              class="font-weight-bold mb-3 p-0"
              style="font-family: 'HangeulNuri-Bold'"
            >
              <strong id="title-1">선택한 장르기반 추천</strong>
            </h3>
            <hr />
            <small class="main-font">개인정보에 입력하신 장르를 기반으로 </small
            ><br /><small class="main-font"
              >{{ name }}님이 좋아하는 장르의 도서를 추천해드립니다.</small
            >
            <br />
            <br />
            <mdb-btn
              v-if="algorithm5.length != 0"
              size="md"
              class="waves-light float-right do"
              @click="goToAlgorithm(algoPack5)"
              style="font-size: small; color: stylish-color"
              >자세히 보기</mdb-btn
            >
            <mdb-btn
              v-else
              disabled
              size="md"
              class="waves-light float-right do"
              style="font-size: small; color: stylish-color"
              >자세히 보기</mdb-btn
            >
          </mdb-col>
        </mdb-row>
        <v-system-bar dark color="#34495e" class="my-5">
          <v-spacer></v-spacer>
        </v-system-bar>
        <mdb-row>
          <mdb-col lg="4" style="margin-top: 3%">
            <a class="pink-text">
              <h6
                class="font-weight-bold mb-3"
                style="font-family: 'HangeulNuri-Bold'; padding-left: 1%"
              >
                For You
              </h6>
            </a>
            <h3
              class="font-weight-bold mb-3 p-0"
              style="font-family: 'HangeulNuri-Bold'"
            >
              <strong id="title-2">{{ age }}대 {{ gender }}을 위한 책</strong>
            </h3>
            <hr />
            <small class="main-font"
              >개인정보에 입력하신 성별, 생년월일을 기반으로 </small
            ><br /><small class="main-font"
              >{{ name }}님에게 알맞는 도서를 추천해드립니다.</small
            >
            <br />
            <br />
            <mdb-btn
              @click="goToAlgorithm(algoPack0)"
              color="pink"
              size="md"
              class="mb-lg-0 mb-4 waves-light do"
              style="font-size: small; color: white"
              >자세히 보기</mdb-btn
            >
          </mdb-col>
          <mdb-col lg="8">
            <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
              <div
                class="uk-position-relative uk-visible-toggle uk-light"
                tabindex="-1"
                uk-slider
              >
                <ul
                  class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
                >
                  <li v-for="algo of algorithm0" :item="algo" :key="algo.id">
                    <mdb-view hover class="zoom">
                      <img
                        v-if="algo.img_url"
                        :src="algo.img_url"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <img
                        v-else
                        src="@/assets/img/no-image.jpg"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <mdb-mask flex-center waves overlay="black-strong">
                        <mdb-btn
                          v-if="algo.title.length > 50"
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title.slice(0, 50) }} ... 자세히
                          보기</mdb-btn
                        >
                        <mdb-btn
                          v-else
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title }} - 자세히 보기</mdb-btn
                        >
                      </mdb-mask>
                    </mdb-view>

                    <div class="uk-position-center uk-panel"></div>
                  </li>
                </ul>

                <a
                  class="uk-position-center-left uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-previous
                  uk-slider-item="previous"
                ></a>
                <a
                  class="uk-position-center-right uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-next
                  uk-slider-item="next"
                ></a>
              </div>

              <a>
                <mdb-mask overlay="white-slight" waves />
              </a>
            </div>
          </mdb-col>
        </mdb-row>
        <v-system-bar dark color="#34495e" class="my-5">
          <v-spacer></v-spacer>
        </v-system-bar>
        <mdb-row>
          <mdb-col v-if="algorithm1.length != 0" lg="8">
            <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
              <div
                class="uk-position-relative uk-visible-toggle uk-light"
                tabindex="-1"
                uk-slider
              >
                <ul
                  class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
                >
                  <li v-for="algo of algorithm1" :item="algo" :key="algo.id">
                    <mdb-view hover class="zoom">
                      <img
                        v-if="algo.img_url"
                        :src="algo.img_url"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <img
                        v-else
                        src="@/assets/img/no-image.jpg"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <mdb-mask flex-center waves overlay="black-strong">
                        <mdb-btn
                          v-if="algo.title.length > 50"
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title.slice(0, 50) }} ... 자세히
                          보기</mdb-btn
                        >
                        <mdb-btn
                          v-else
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title }} - 자세히 보기</mdb-btn
                        >
                      </mdb-mask>
                    </mdb-view>

                    <div class="uk-position-center uk-panel"></div>
                  </li>
                </ul>

                <a
                  class="uk-position-center-left uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-previous
                  uk-slider-item="previous"
                ></a>
                <a
                  class="uk-position-center-right uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-next
                  uk-slider-item="next"
                ></a>
              </div>
              <a>
                <mdb-mask overlay="white-slight" waves />
              </a>
            </div>
          </mdb-col>
          <mdb-col v-else lg="8" class="no-data1 my-auto">
            <h4 style="font-family: HangeulNuri-Bold">
              좋아요한 책이 부족합니다.
            </h4>
            <p style="font-family: HangeulNuri-Bold">
              책에 좋아요를 해주시면 해당 추천이 활성화됩니다.
            </p>
          </mdb-col>
          <mdb-col lg="4" style="margin-top: 3%" class="text-right">
            <h6
              class="font-weight-bold mb-3"
              style="font-family: 'HangeulNuri-Bold'"
            >
              Description
            </h6>

            <h3
              class="font-weight-bold mb-3 p-0"
              style="font-family: 'HangeulNuri-Bold'"
            >
              <strong id="title-1">줄거리 기반 도서 추천</strong>
            </h3>

            <hr />
            <small class="main-font"
              >선호하는 책에 '좋아요'를 표시해주세요.</small
            ><br /><small class="main-font"
              >{{ name }}님이 좋아할 줄거리의 도서를 추천해드립니다.</small
            >
            <br />
            <br />
            <mdb-btn
              v-if="algorithm1.length != 0"
              color="success do"
              size="md"
              class="waves-light text-right"
              @click="goToAlgorithm(algoPack1)"
              style="font-size: small; color: white"
              >자세히 보기</mdb-btn
            >
            <mdb-btn
              v-else
              disabled
              color="success do"
              size="md"
              class="waves-light text-right"
              style="font-size: small; color: white"
              >자세히 보기</mdb-btn
            >
          </mdb-col>
        </mdb-row>
        <v-system-bar dark color="#34495e" class="my-5">
          <v-spacer></v-spacer>
        </v-system-bar>
        <mdb-row>
          <mdb-col lg="4" style="margin-top: 3%">
            <a class="pink-text">
              <h6
                class="font-weight-bold mb-3"
                style="font-family: 'HangeulNuri-Bold'"
              >
                Topic
              </h6>
            </a>
            <h3
              class="font-weight-bold mb-3 p-0"
              style="font-family: 'HangeulNuri-Bold'"
            >
              <strong id="title-2">선호하는 주제의 도서 추천</strong>
            </h3>
            <hr />
            <small class="main-font"
              >마음에 드는 책이 있다면?? '좋아요' 해주세요. </small
            ><br /><small class="main-font"
              >{{ name }}님이 좋아하는 주제의 도서를 추천해드립니다.</small
            >
            <br />
            <br />
            <mdb-btn
              v-if="algorithm3.length != 0"
              @click="goToAlgorithm(algoPack3)"
              color="yellow"
              size="md"
              class="mb-lg-0 mb-4 waves-light do"
              style="font-size: small; color: white"
              >자세히 보기</mdb-btn
            >
            <mdb-btn
              v-else
              disable
              color="yellow"
              size="md"
              class="mb-lg-0 mb-4 waves-light do"
              style="font-size: small; color: white"
              >자세히 보기</mdb-btn
            >
          </mdb-col>
          <mdb-col v-if="algorithm3.length != 0" lg="8">
            <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
              <div
                class="uk-position-relative uk-visible-toggle uk-light"
                tabindex="-1"
                uk-slider
              >
                <ul
                  class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
                >
                  <li v-for="algo of algorithm3" :item="algo" :key="algo.id">
                    <mdb-view hover class="zoom">
                      <img
                        v-if="algo.img_url"
                        :src="algo.img_url"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <img
                        v-else
                        src="@/assets/img/no-image.jpg"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <mdb-mask flex-center waves overlay="black-strong">
                        <mdb-btn
                          v-if="algo.title.length > 50"
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title.slice(0, 50) }} ... 자세히
                          보기</mdb-btn
                        >
                        <mdb-btn
                          v-else
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title }} - 자세히 보기</mdb-btn
                        >
                      </mdb-mask>
                    </mdb-view>

                    <div class="uk-position-center uk-panel"></div>
                  </li>
                </ul>

                <a
                  class="uk-position-center-left uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-previous
                  uk-slider-item="previous"
                ></a>
                <a
                  class="uk-position-center-right uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-next
                  uk-slider-item="next"
                ></a>
              </div>

              <a>
                <mdb-mask overlay="white-slight" waves />
              </a>
            </div>
          </mdb-col>
          <mdb-col v-else lg="8" class="no-data2 my-auto">
            <h4 style="font-family: HangeulNuri-Bold">
              좋아요한 책이 부족합니다.
            </h4>
            <p style="font-family: HangeulNuri-Bold">
              책에 좋아요를 해주시면 해당 추천이 활성화됩니다.
            </p>
          </mdb-col>
        </mdb-row>
        <v-system-bar dark color="#34495e" class="my-5">
          <v-spacer></v-spacer>
        </v-system-bar>
        <mdb-row>
          <mdb-col v-if="algorithm2.length != 0" lg="8">
            <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
              <div
                class="uk-position-relative uk-visible-toggle uk-light"
                tabindex="-1"
                uk-slider
              >
                <ul
                  class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
                >
                  <li v-for="algo of algorithm2" :item="algo" :key="algo.id">
                    <mdb-view hover class="zoom">
                      <img
                        v-if="algo.img_url"
                        :src="algo.img_url"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <img
                        v-else
                        src="@/assets/img/no-image.jpg"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <mdb-mask flex-center waves overlay="black-strong">
                        <mdb-btn
                          v-if="algo.title.length > 50"
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title.slice(0, 50) }} ... 자세히
                          보기</mdb-btn
                        >
                        <mdb-btn
                          v-else
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title }} - 자세히 보기</mdb-btn
                        >
                      </mdb-mask>
                    </mdb-view>

                    <div class="uk-position-center uk-panel"></div>
                  </li>
                </ul>

                <a
                  class="uk-position-center-left uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-previous
                  uk-slider-item="previous"
                ></a>
                <a
                  class="uk-position-center-right uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-next
                  uk-slider-item="next"
                ></a>
              </div>
              <a>
                <mdb-mask overlay="white-slight" waves />
              </a>
            </div>
          </mdb-col>
          <mdb-col v-else lg="8" class="no-data1 my-auto">
            <h4 style="font-family: HangeulNuri-Bold">
              작성한 리뷰가 없습니다.
            </h4>
            <p style="font-family: HangeulNuri-Bold">
              리뷰를 작성해주시면 해당 추천이 활성화됩니다.
            </p>
          </mdb-col>
          <mdb-col lg="4" style="margin-top: 3%" class="text-right">
            <h6
              class="font-weight-bold mb-3"
              style="font-family: 'HangeulNuri-Bold'"
            >
              About Review
            </h6>
            <h3
              class="font-weight-bold mb-3 p-0"
              style="font-family: 'HangeulNuri-Bold'"
            >
              <strong id="title-1">작성한 리뷰 기반의 도서 추천</strong>
            </h3>
            <hr />
            <small class="main-font">책에 대한 리뷰를 남겨보세요! </small
            ><br /><small class="main-font"
              >{{ name }}님이 작성한 리뷰를 기반으로 도서를
              추천해드립니다.</small
            >
            <br />
            <br />
            <mdb-btn
              v-if="algorithm2.length != 0"
              color="indigo"
              size="md"
              class="waves-light do"
              @click="goToAlgorithm(algoPack2)"
              style="font-size: small; color: white"
              >자세히 보기</mdb-btn
            >
            <mdb-btn
              v-else
              disabled
              color="indigo"
              size="md"
              class="waves-light do"
              style="font-size: small; color: white"
              >자세히 보기</mdb-btn
            >
          </mdb-col>
        </mdb-row>
        <v-system-bar dark color="#34495e" class="my-5">
          <v-spacer></v-spacer>
        </v-system-bar>
        <mdb-row>
          <mdb-col lg="4" style="margin-top: 3%">
            <a class="pink-text">
              <h6
                class="font-weight-bold mb-3"
                style="font-family: 'HangeulNuri-Bold'"
              >
                People
              </h6>
            </a>
            <h3
              class="font-weight-bold mb-3 p-0"
              style="font-family: 'HangeulNuri-Bold'"
            >
              <strong id="title-2">나와 비슷한 사용자들이 읽은</strong
              ><br /><strong>도서 추천</strong>
            </h3>
            <hr />
            <small class="main-font">나와 취향이 같은 사람은 ?</small
            ><br /><small class="main-font"
              >{{ name }}님과 비슷한 성향의 사람이 좋아하는 도서를
              추천해드립니다.</small
            >
            <br />
            <br />
            <mdb-btn
              v-if="algorithm1.length != 0"
              @click="goToAlgorithm(algoPack4)"
              size="md"
              class="mb-lg-0 mb-4 waves-light do"
              style="
                font-size: small;
                color: white;
                background-color: #2e2e2e !important;
              "
              >자세히 보기</mdb-btn
            >
            <mdb-btn
              v-else
              disabled
              size="md"
              class="mb-lg-0 mb-4 waves-light do"
              style="
                font-size: small;
                color: white;
                background-color: #2e2e2e !important;
              "
              >자세히 보기</mdb-btn
            >
          </mdb-col>
          <mdb-col v-if="algorithm1.length != 0" lg="8">
            <div class="rounded z-depth-2 mb-lg-0 mb-4" hover>
              <div
                class="uk-position-relative uk-visible-toggle uk-light"
                tabindex="-1"
                uk-slider
              >
                <ul
                  class="uk-slider-items uk-child-width-1-2 uk-child-width-1-3@s uk-child-width-1-4@m"
                >
                  <li v-for="algo of algorithm4" :item="algo" :key="algo.id">
                    <mdb-view hover class="zoom">
                      <img
                        v-if="algo.img_url"
                        :src="algo.img_url"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <img
                        v-else
                        src="@/assets/img/no-image.jpg"
                        alt="bookImage"
                        class="bookimage"
                      />
                      <mdb-mask flex-center waves overlay="black-strong">
                        <mdb-btn
                          v-if="algo.title.length > 50"
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title.slice(0, 50) }} ... 자세히
                          보기</mdb-btn
                        >
                        <mdb-btn
                          v-else
                          outline="white"
                          @click="gotoDetail(algo.id)"
                          style="
                            width: 220px;
                            height: 300px;
                            font-size: large;
                            font-family: HangeulNuri-Bold;
                          "
                          >{{ algo.title }} - 자세히 보기</mdb-btn
                        >
                      </mdb-mask>
                    </mdb-view>

                    <div class="uk-position-center uk-panel"></div>
                  </li>
                </ul>

                <a
                  class="uk-position-center-left uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-previous
                  uk-slider-item="previous"
                ></a>
                <a
                  class="uk-position-center-right uk-position-small uk-hidden-hover"
                  style="color: white"
                  href="#"
                  uk-slidenav-next
                  uk-slider-item="next"
                ></a>
              </div>

              <a>
                <mdb-mask overlay="white-slight" waves />
              </a>
            </div>
          </mdb-col>
          <mdb-col v-else lg="8" class="my-auto no-data2">
            <h4 style="font-family: HangeulNuri-Bold">
              좋아요한 책이 부족합니다.
            </h4>
            <p style="font-family: HangeulNuri-Bold">
              책에 좋아요를 해주시면 해당 추천이 활성화됩니다.
            </p>
          </mdb-col>
        </mdb-row>
        <v-system-bar dark color="#34495e" class="my-5">
          <v-spacer></v-spacer>
        </v-system-bar>
        <br />
        <br />
        <br />
        <br />
      </div>
      <div v-else class="loading">
        <div class="spinner-grow text-primary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-secondary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-success" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-danger" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-warning" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-info" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-light" role="status">
          <span class="sr-only">Loading...</span>
        </div>
        <div class="spinner-grow text-dark" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </mdb-container>

    <v-btn
      v-scroll="onScroll"
      v-show="fab"
      fab
      dark
      fixed
      bottom
      right
      color="#34495e"
      @click="toTop"
    >
      <v-icon>mdi-arrow-up-thick</v-icon>
    </v-btn>
  </div>
</template>

<script>
import swal from "sweetalert";
import VueCookies from "vue-cookies";
import { mdbContainer, mdbRow, mdbCol, mdbMask, mdbBtn, mdbView } from "mdbvue";
import axios from "axios";

export default {
  name: "Main",
  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbMask,
    mdbBtn,
    mdbView,
  },
  beforeRouteEnter(to, from, next) {
    if (!VueCookies.get("jwt_token")) {
      next("/");
      // swal("잘못된 접근입니다.3")
    } else {
      next();
    }
  },
  created() {
    if (sessionStorage.getItem("data") === null) {
      sessionStorage.setItem("data", "false");
    }

    if (sessionStorage.getItem("data2") === null) {
      sessionStorage.setItem("data2", "false");
    }
    if (sessionStorage.getItem("data") === "false") {
      // 프로필 정보 가져오기
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/analyze/feature_temp/`, {
          headers: {
            Authorization: VueCookies.get("jwt_token"),
          },
        })
        .then((res) => {
          // console.log("유저정보 가져오기");
          // console.log(res);
          // this.age = parseInt(res.data.info.age / 365);
          this.age = res.data.info.age;
          var rest = this.age % 10;
          this.age = this.age - rest;

          if (res.data.info.gender == 0) {
            this.gender = "남성";
          } else {
            this.gender = "여성";
          }
          this.name = res.data.info.name;
          this.algorithm0 = res.data.feature;
          if (this.age != 0) {
            this.algoPack0["theme"] =
              this.age + "대" + this.gender + "을 위한 책";
          } else {
            this.algoPack0["theme"] = "어린이를 위한 책";
          }

          this.algoPack0["algo"] = this.algorithm0;
          this.algoPack0["num"] = 0;

          sessionStorage.setItem("data", JSON.stringify(res));
        });
      // .catch((err) => {
      //   console.log(err);
      // });
      this.isLoading = true;
      let today = new Date();

      let y = today.getFullYear(); // 년도
      let m = today.getMonth() + 1; // 월
      let d = today.getDate(); // 날짜
      this.year = y;
      this.month = m;
      this.day = d;
    } else {
      const data = JSON.parse(sessionStorage.getItem("data"));

      // this.age = parseInt(data.data.info.age / 365);
      this.age = data.data.info.age;
      var rest = this.age % 10;
      this.age = this.age - rest;
      if (data.data.info.gender == 0) {
        this.gender = "남성";
      } else {
        this.gender = "여성";
      }
      this.name = data.data.info.name;
      this.algorithm0 = data.data.feature;
      if (this.age != 0) {
        this.algoPack0["theme"] = this.age + "대" + this.gender + "을 위한 책";
      } else {
        this.algoPack0["theme"] = "어린이를 위한 책";
      }
      this.algoPack0["algo"] = this.algorithm0;
      this.algoPack0["num"] = 0;

      this.isLoading = true;
      let today = new Date();

      let y = today.getFullYear(); // 년도
      let m = today.getMonth() + 1; // 월
      let d = today.getDate(); // 날짜
      this.year = y;
      this.month = m;
      this.day = d;
    }

    if (sessionStorage.getItem("data2") === "false") {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/analyze/recommend_temp/`, {
          // Back에서 원하는 데이터
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then((res) => {
          // console.log("알고리즘 모두 가져오기");
          // console.log(res);
          this.algorithm1 = res.data.desc;
          if (this.algorithm1) {
            this.algoPack1["theme"] = "책 줄거리기반 도서 추천";
            this.algoPack1["algo"] = this.algorithm1;
            this.algoPack1["num"] = 1;
          }

          this.algorithm2 = res.data.review;
          if (this.algorithm2) {
            this.algoPack2["theme"] = "작성한 리뷰 기반의 도서 추천";
            this.algoPack2["algo"] = this.algorithm2;
            this.algoPack2["num"] = 2;
          }

          this.algorithm3 = res.data.title;
          if (this.algorithm3) {
            this.algoPack3["theme"] = "선호하는 주제의 도서 추천";
            this.algoPack3["algo"] = this.algorithm3;
            this.algoPack3["num"] = 3;
          }

          this.algorithm4 = res.data.others;
          if (this.algorithm4) {
            this.algoPack4["theme"] = "나와 비슷한 사용자들이 읽은 책 ";
            this.algoPack4["algo"] = this.algorithm4;
            this.algoPack4["num"] = 4;
            this.isLoading = false;
          }

          this.algorithm5 = res.data.genres;
          if (this.algorithm5) {
            this.algoPack5["theme"] = "선호하는 장르 추천";
            this.algoPack5["algo"] = res.algorithm5;
            this.algoPack5["num"] = 5;
          }
          this.isLoading = false;

          sessionStorage.setItem("data2", JSON.stringify(res));
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    } else {
      const data = JSON.parse(sessionStorage.getItem("data2"));

      this.algorithm1 = data.data.desc;
      this.algoPack1["theme"] = "좋아요한 도서의 줄거리기반 추천";
      this.algoPack1["algo"] = this.algorithm1;
      this.algoPack1["num"] = 1;

      this.algorithm2 = data.data.review;
      this.algoPack2["theme"] = "작성한 리뷰 기반의 도서 추천";
      this.algoPack2["algo"] = this.algorithm2;
      this.algoPack2["num"] = 2;

      this.algorithm3 = data.data.title;
      this.algoPack3["theme"] = "좋아요한 도서와 비슷한 주제의 도서 추천";
      this.algoPack3["algo"] = this.algorithm3;
      this.algoPack3["num"] = 3;
      this.isLoading = false;

      this.algorithm4 = data.data.others;
      this.algoPack4["theme"] = "나와 유사한 사용자들이 읽은 도서 추천 ";
      this.algoPack4["algo"] = this.algorithm4;
      this.algoPack4["num"] = 4;
      this.isLoading = false;

      this.algorithm5 = data.data.genres;
      this.algoPack5["theme"] = "선호하는 장르 도서 추천";
      this.algoPack5["algo"] = this.algorithm5;
      this.algoPack5["num"] = 5;
      this.isLoading = false;
    }

    if (VueCookies.get("user_gender") == 2) {
      swal("잘못된 접근입니다.", "회원가입이 완료되지 않았습니다.");
      this.$router.push("/signup");
    }
    // 알고리즘1
    this.$vuetify.goTo(0);
  },

  data() {
    return {
      algoPack0: {},
      algoPack1: {},
      algoPack2: {},
      algoPack3: {},
      algoPack4: {},
      algoPack5: {},
      name: null,
      age: null,
      gender: 0,

      algorithm0: null,
      algorithm1: null,
      algorithm2: null,
      algorithm3: null,
      algorithm4: null,
      algorithm5: null,

      isLoading: false,
      // 스크롤
      fab: false,
    };
  },
  methods: {
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
    goToAlgorithm(algo) {
      this.$emit("goToAlgorithm", algo);
      this.$router.push(`/algo/${algo.num}`);
    },

    gotoDetail(id) {
      this.$router.push(`/bookdetail/${id}`);
    },
  },
};
</script>

<style scoped>
.main-font {
  font-family: "HangeulNuri-Bold";
}
[v-cloak] {
  display: none;
}
.loading {
  text-align: center;
  color: black;
  z-index: 2;
  padding: 8px 18px;
  border-radius: 5px;
  left: calc(50% - 105px);
  top: calc(50% - 45px);
}

@font-face {
  font-family: "HangeulNuri-Bold";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_three@1.0/HangeulNuri-Bold.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
  font-size: x-large;
}
.do {
  font-family: "Do Hyeon", sans-serif;
}
.bookimage {
  width: 200px;
  height: 300px;
  display: block;
  margin: 0px auto;
}
.waves-light.float-right.btn.btn-default.btn-md.ripple-parent {
  background-color: #9933cc !important;
  color: white;
}

.no-data1 {
  text-align: start;
}

.no-data2 {
  text-align: end;
}
</style>
