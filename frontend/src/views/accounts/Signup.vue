<template>
  <div id="dmap" class="tma mt-5 mx-auto">
    <h1 class="my-5 text-center nohover">
      ✏<spanl class="main-font ml-3">회원가입</spanl>
    </h1>
    <v-system-bar color="#009688" class="rounded-t-xl">
      <v-spacer></v-spacer>
    </v-system-bar>
    <v-stepper v-model="e1" :alt-labels="true">
      <v-stepper-header>
        <v-stepper-step
          :complete="e1 > 1"
          step="1"
          color="#009688"
          class="main-font"
          >기본정보</v-stepper-step
        >
        <v-divider></v-divider>

        <v-stepper-step
          :complete="e1 > 2"
          step="2"
          color="#009688"
          class="main-font"
          >상세정보</v-stepper-step
        >
        <v-divider></v-divider>

        <v-stepper-step
          :complete="e1 > 3"
          step="3"
          color="#009688"
          class="main-font"
          >좋아하는 장르</v-stepper-step
        >
        <v-divider></v-divider>

        <v-stepper-step step="4" color="#009688" class="main-font"
          >좋아하는 책</v-stepper-step
        >
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-card
            class="mb-12"
            color
            height="100%"
            width="100%"
            min-height="700px"
          >
            <v-container>
              <v-row class>
                <v-col cols="12" md="6">
                  <img src="@/assets/img/step1.jpg" alt />
                </v-col>
                <v-col cols="12" md="6">
                  <v-form
                    ref="form1"
                    v-model="valid1"
                    :lazy-validation="lazy1"
                    class="form-width"
                  >
                    <v-row>
                      <!-- 이메일 -->
                      <v-col cols="9">
                        <v-text-field
                          v-model="email"
                          :value="email"
                          label="아이디"
                          :rules="emailRules"
                          suffix="@bookridge.com"
                          required
                          class="main-font"
                          color="#009688"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="3">
                        <v-btn
                          class="mt-4 main-font"
                          v-if="email == ''"
                          text
                          outlined
                          color="success"
                          :disabled="true"
                          >중복확인</v-btn
                        >
                        <v-btn
                          class="mt-4"
                          v-else
                          text
                          outlined
                          color="success"
                          @click="checkEmail"
                          >중복확인</v-btn
                        >
                      </v-col>
                    </v-row>
                    <v-row class="ml-1">
                      <p
                        class="text-green text-caption main-font"
                        v-if="checkedEmail == email && isCheckedEmail"
                      >
                        사용가능한 아이디입니다.
                      </p>
                      <p v-else class="text-red text-caption main-font">
                        아이디 중복확인이 필요합니다.
                      </p>
                    </v-row>
                    <!-- 이름 -->
                    <v-text-field
                      v-model="name"
                      :counter="10"
                      :rules="nameRules"
                      label="이름"
                      required
                      class="main-font"
                      color="#009688"
                    ></v-text-field>
                    <!-- 비밀번호 -->
                    <v-text-field
                      v-model="password1"
                      :rules="password1Rules"
                      label="비밀번호"
                      required
                      counter
                      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="show1 ? 'text' : 'password'"
                      @click:append="show1 = !show1"
                      color="#009688"
                    ></v-text-field>
                    <v-text-field
                      v-model="password2"
                      :rules="password2Rules"
                      label="비밀번호 확인"
                      required
                      counter
                      :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="show2 ? 'text' : 'password'"
                      @click:append="show2 = !show2"
                      color="#009688"
                    ></v-text-field>
                    <v-divider></v-divider>
                    <div class="d-flex justify-end mt-5">
                      <v-btn
                        class="mr-3 main-font"
                        text
                        outlined
                        color="success"
                        @click="goToHome"
                        >홈페이지로 돌아가기</v-btn
                      >
                      <v-btn
                        class="main-font"
                        text
                        outlined
                        color="success"
                        :disabled="!valid1 || !isCheckedEmail"
                        @click="firstStep"
                        >다음 단계</v-btn
                      >
                    </div>
                  </v-form>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-card
            class="mb-12"
            color
            height="100%"
            width="100%"
            min-height="700px"
          >
            <v-container>
              <v-row class>
                <v-col cols="12" md="6">
                  <img src="@/assets/img/step2.jpg" style="width:100% height:500px" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-form
                    ref="form2"
                    v-model="valid2"
                    :lazy-validation="lazy2"
                    class="form-width"
                  >
                    <!-- 성별 -->
                    <v-select
                      v-model="gender"
                      :items="genders"
                      :rules="genderRules"
                      label="성별"
                      required
                      class="mb-3 main-font"
                      colo
                    ></v-select>

                    <!-- 생년월일 -->
                    <v-menu
                      ref="menu"
                      v-model="menu"
                      :close-on-content-click="false"
                      transition="scale-transition"
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          :rules="birthdayRules"
                          v-model="birth"
                          label="생년월일"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                          class="main-font"
                        ></v-text-field>
                      </template>
                      <v-date-picker
                        class="main-font"
                        locale="south-korea"
                        color="#009688"
                        ref="picker"
                        v-model="birth"
                        :max="new Date().toISOString().substr(0, 10)"
                        min="1950-01-01"
                        @change="save"
                      ></v-date-picker>
                    </v-menu>
                    <!-- 주소 -->
                    <v-text-field
                      type="text"
                      v-model="address"
                      disabled
                      id="sample5_address"
                      :rules="addressRules"
                      class="main-font"
                    ></v-text-field>
                    <v-text-field
                      type="text"
                      v-show="hide"
                      id="x"
                      placeholder="주소"
                      disabled
                    ></v-text-field>
                    <v-text-field
                      type="text"
                      v-show="hide"
                      id="y"
                      placeholder="주소"
                      disabled
                    ></v-text-field>
                    <input
                      ref="checkRules"
                      type="button"
                      onclick="sample5_execDaumPostcode()"
                      value="주소 검색"
                      class="mr-3 address-btn main-font"
                      uk-tooltip="버튼을 클릭해주세요."
                    />
                    <v-checkbox
                      v-model="checkbox"
                      :rules="agreeRules"
                      label="약관 동의"
                      required
                      @click="checkRules"
                      class="main-font"
                    ></v-checkbox>
                    <v-dialog v-model="dialogPolicy" width="700">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          class="main-font"
                          text
                          color="#009688"
                          dark
                          v-bind="attrs"
                          v-on="on"
                          >서비스 이용 약관</v-btn
                        >
                      </template>

                      <v-card width="100%">
                        <v-card-title
                          class="d-flex justify-content-center"
                          style="background-color: #009688"
                          ><h3 class="main-font" style="color: white">
                            서비스 이용약관
                          </h3></v-card-title
                        >
                        <v-card-text class="mt-5 main-font"
                          >저희 '북릿지' 서비스는 도서 추천 웹
                          서비스입니다.</v-card-text
                        >
                        <v-card-text class="mt-5 main-font"
                          >북릿지는 「개인정보보호법」 제30조(개인정보
                          처리방침의 수립 및 공개)에 따라 정보주체의 개인정보와
                          권익을 보호하고, 개인정보와 관련한 정보주체의 고충을
                          신속하고 원활하게 처리할 수 있도록 다음과 같이
                          개인정보 처리방침을 수립·공개합니다.</v-card-text
                        >
                        <v-card-text class="mt-5 main-font"
                          >이 방침은 별도의 설명이 없는 한 북릿지에서 처리하는
                          모든 개인정보 파일에 적용됩니다. 다만, 소관 업무
                          처리를 위해 각 부서에서 별도의 개인정보 처리방침을
                          제정·시행하는 경우 그 방침에 따르고 해당 부서가
                          운영하는 별도 홈페이지에 게시함을
                          알려드립니다.</v-card-text
                        >
                        <v-card-text class="mt-5 main-font"
                          >또한, 관련 법령에서 규정한 바에 따라 보유하고 있는
                          개인정보에 대한 열람청구권과 정정청구권 등 이용자의
                          권익을 존중합니다. 정보주체는 이러한 법령상 권익의
                          침해 등에 대하여 행정심판법이 정하는 바에 따라
                          행정심판을 청구할 수 있으며, 개인정보 분쟁조정위원회,
                          개인정보 침해신고센터 등에 분쟁해결이나 상담 등을
                          신청할 수 있습니다.</v-card-text
                        >
                        <v-card-text class="mt-5 main-font">
                          <h4 class="main-font">
                            <v-icon>mdi-pencil</v-icon>제1조. 개인정보의 처리
                            목적·항목 및 보유기간
                          </h4>
                          <p>
                            북릿지는 정보주체의 동의 또는 관련 법령에 따라 필요
                            최소한의 개인정보를 수집하며, 처리 목적 및
                            보유·이용기간 내에서 개인정보를 처리·보유합니다.
                          </p>
                          <p>
                            구미시는 법령에 따른 개인정보 보유·이용기간 또는
                            정보주체로부터 개인정보를 수집할 때 동의받은
                            보유·이용기간 내에서 개인정보를 처리·보유합니다.
                          </p>
                        </v-card-text>
                        <v-card-text class="mt-5 main-font">
                          <h4 class="main-font">
                            <v-icon>mdi-pencil</v-icon>제2조. 개인정보의 제3자
                            제공에 관한 사항
                          </h4>
                          <p>
                            북릿지는 원칙적으로 정보주체의 개인정보를 수집․이용
                            목적으로 명시한 범위 내에서 처리하며 이용자의 사전
                            동의 없이는 본래의 범위를 초과하여 처리하거나
                            제3자에게 제공하지 않습니다.
                          </p>
                          <p>
                            입력하신 개인정보는 오로지 추천 서비스를 위해
                            사용됨을 알립니다.
                          </p>
                        </v-card-text>
                        <v-card-text class="mt-5 main-font"
                          >감사합니다.</v-card-text
                        >

                        <v-divider></v-divider>

                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                            class="main-font"
                            color="success"
                            text
                            @click="dialogPolicy = false"
                            >확인</v-btn
                          >
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                    <v-divider></v-divider>
                    <div class="d-flex justify-end my-5">
                      <v-btn
                        text
                        outlined
                        class="mr-3 main-font"
                        color="success"
                        @click="e1 = 1"
                        v-show="!isSocial"
                        >이전 단계</v-btn
                      >
                      <v-btn
                        text
                        outlined
                        class="mr-3 main-font"
                        color="success"
                        @click="goToHome"
                        v-show="isSocial"
                        >홈페이지로 돌아가기</v-btn
                      >
                      <v-btn
                        class="main-font"
                        text
                        outlined
                        color="success"
                        :disabled="!valid2"
                        @click="e1 = 3"
                        >다음 단계</v-btn
                      >
                    </div>
                  </v-form>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>

        <v-stepper-content step="3">
          <v-card
            class="mb-12"
            color
            height="100%"
            width="100%"
            min-height="700px"
          >
            <v-container fluid>
              <h3 class="text-center main-font">
                좋아하는 장르를 선택해주세요.
              </h3>
              <h6 class="text-center main-font">다수 선택이 가능합니다.</h6>
              <v-container class="pa-4 text-center">
                <v-row
                  no-gutters
                  class="fill-height"
                  align="center"
                  justify="center"
                >
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(1)"
                      >
                        <v-img
                          src="@/assets/img/philosophy.png"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                철학
                                <span v-if="genre1" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title>
                        </v-img>
                      </v-card>
                    </v-hover>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(2)"
                      >
                        <v-img
                          src="@/assets/img/religion.jpg"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                종교
                                <span v-if="genre2" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title></v-img
                        >
                      </v-card>
                    </v-hover>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(3)"
                      >
                        <v-img
                          src="@/assets/img/society.jpg"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                사회과학
                                <span v-if="genre3" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title></v-img
                        >
                      </v-card>
                    </v-hover>
                  </v-col>
                </v-row>
                <v-row no-gutters>
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(4)"
                      >
                        <v-img
                          src="@/assets/img/science.jpg"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                순수과학
                                <span v-if="genre4" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title></v-img
                        >
                      </v-card>
                    </v-hover>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(5)"
                      >
                        <v-img
                          src="@/assets/img/technology.png"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                기술과학
                                <span v-if="genre5" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title></v-img
                        >
                      </v-card>
                    </v-hover>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(6)"
                      >
                        <v-img
                          src="@/assets/img/artist.jpg"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                예술
                                <span v-if="genre6" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title></v-img
                        >
                      </v-card>
                    </v-hover>
                  </v-col>
                </v-row>
                <v-row no-gutters>
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(7)"
                      >
                        <v-img
                          src="@/assets/img/language.jpg"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                언어
                                <span v-if="genre7" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title></v-img
                        >
                      </v-card>
                    </v-hover>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(8)"
                      >
                        <v-img
                          src="@/assets/img/literature.jpg"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                문학
                                <span v-if="genre8" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title></v-img
                        >
                      </v-card>
                    </v-hover>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-hover v-slot:default="{ hover }">
                      <v-card
                        class="pa-2 basic"
                        :elevation="hover ? 12 : 2"
                        :class="{ 'on-hover': hover }"
                        outlined
                        tile
                        @click="onSelectImage(9)"
                      >
                        <v-img
                          src="@/assets/img/history.png"
                          aspect-ratio="1"
                          height="225px"
                        >
                          <v-card-title class="title white--text">
                            <v-row class="fill-height d-flex flex-column">
                              <p
                                class="mt-4 subheading text-center black pl-5 main-font"
                              >
                                역사
                                <span v-if="genre9" class="text-right"
                                  ><v-icon color="white"
                                    >mdi-check-bold</v-icon
                                  ></span
                                >
                                <span v-else class="text-right"
                                  ><v-icon>mdi-check-bold</v-icon></span
                                >
                              </p>
                            </v-row>
                          </v-card-title></v-img
                        >
                      </v-card>
                    </v-hover>
                  </v-col>
                </v-row>
              </v-container>
              <v-divider></v-divider>
              <v-row class="d-flex justify-content-center">
                <v-btn
                  class="mr-1 main-font"
                  text
                  outlined
                  color="success"
                  @click="e1 = 2"
                  >이전 단계</v-btn
                >
                <v-btn
                  class="main-font"
                  text
                  outlined
                  color="success"
                  @click="e1 = 4"
                  >다음 단계</v-btn
                >
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>
        <v-stepper-content step="4">
          <v-card
            class="mb-12"
            color
            height="100%"
            width="100%"
            min-height="700px"
          >
            <v-container fluid>
              <h3 class="text-center main-font my-5">
                읽었던 책 중 감명깊었던 책을 입력해주세요.
              </h3>
              <h6 class="main-font text-center">
                * 최대 10개까지 등록가능합니다.
              </h6>
              <v-row class="d-flex justify-content-center mt-5">
                <v-text-field
                  class="pt-5 main-font"
                  style="max-width: 700px"
                  v-model="searchWord"
                  @keyup="bookSearch"
                  label="도서를 검색해주세요."
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
                  sm="6"
                  xs="6"
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
                      <div v-if="book.description" style="height: 100px">
                        <small v-show="book.description.length > 60">
                          {{ book.description.slice(0, 60) }}...
                        </small>
                        <small v-show="book.description.length <= 60">
                          {{ book.description }}
                        </small>
                      </div>
                      <div v-else style="height: 100px">
                        <small>줄거리에 대한 정보가 없는 책입니다.</small>
                      </div>
                      <v-row class="mt-5 d-flex justify-content-center">
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
              <v-divider></v-divider>
              <v-row style="width: 100%">
                <v-col cols="2" class="main-font text-center">
                  책 이미지
                </v-col>
                <v-col cols="8" class="main-font text-center"> 책 제목 </v-col>
                <v-col cols="2" class="main-font text-center">
                  선택 취소
                </v-col>
              </v-row>
              <v-divider></v-divider>
              <div v-if="selectedBooks.length != 0">
                <v-row v-for="book in selectedBooks" :key="book.id">
                  <v-col cols="2" class="text-center"
                    ><v-img
                      v-if="book.img_url"
                      class="book-image"
                      :src="book.img_url"
                    ></v-img>
                    <v-img
                      v-else
                      class="book-image"
                      src="@/assets/img/no-image.jpg"
                    ></v-img>
                  </v-col>
                  <v-col cols="8" class="text-center">
                    <h6 v-if="book.title" class="main-font text-center">
                      {{ book.title }}
                    </h6>
                    <h6 v-else class="main-font text-center">
                      제목이 없는 책입니다.
                    </h6>
                  </v-col>
                  <v-col cols="2" class="text-center">
                    <v-btn text @click="cancelBook(book)" uk-tooltip="선택 취소"
                      ><v-icon>mdi-delete</v-icon></v-btn
                    >
                  </v-col>
                </v-row>
              </div>
              <div v-else class="flex-column justify-content-center">
                <v-row class="d-flex justify-content-center">
                  <h3
                    class="main-font d-flex align-items-center"
                    style="min-height: 300px"
                  >
                    선택하신 책이 없습니다.
                  </h3>
                </v-row>
              </div>
              <v-divider></v-divider>
              <v-row class="d-flex justify-content-start ml-5 main-font">
                선택한 도서 개수 : {{ selectedBooks.length }} / 10
              </v-row>
              <v-divider></v-divider>
              <v-row class="d-flex justify-content-center">
                <v-btn
                  class="mr-1 main-font"
                  text
                  outlined
                  color="success"
                  @click="e1 = 3"
                  >이전 단계</v-btn
                >
                <v-btn
                  class="ml-1 main-font"
                  text
                  outlined
                  :disabled="selectedBooks.length > 10"
                  color="success"
                  @click="submit"
                  >가입</v-btn
                >
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";
import swal from "sweetalert";

export default {
  name: "Signup",
  watch: {
    email() {
      return (this.email = this.email.replace(/[^a-z0-9]/gi, ""));
    },
    menu(val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = "YEAR"));
    },
  },

  created() {
    if (VueCookies.get("user_gender") == 2) {
      this.el = 2;
    }
    this.isLogin = false;
    if (VueCookies.get("jwt_token")) {
      // console.log(VueCookies.get("jwt_token"));
      this.e1 = 2;
      this.isSocial = true;
    } else {
      this.e1 = 1;
    }
  },

  methods: {
    // 책 선택
    selectBook(book) {
      if (this.selectedBooks.length < 10) {
        if (this.choice.indexOf(book) == -1) {
          this.selectedBooks.push(book);
          this.choice.push(book);
          // console.log(book);
        } else {
          swal("이미 선택한 책입니다.");
        }
      } else {
        swal("이미 10개의 도서를 추가하셨습니다.");
      }
    },
    // 선택 취소
    cancelBook(book) {
      this.selectedBooks.splice(this.selectedBooks.indexOf(book), 1);
      this.selectedBooks = [...this.selectedBooks];
      this.choice.splice(this.choice.indexOf(book), 1);
      this.choice = [...this.choice];
    },
    // 자동완성
    bookSearch() {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/books/book_auto_search/`, {
          params: {
            search_word: this.searchWord,
          },
        })
        .then((res) => {
          // console.log("검색 결과");
          // console.log(res);
          this.autoBooks = res.data.result;
        })
        // .catch((err) => {
        //   console.log(err);
        // });
    },

    firstStep() {
      axios
        .post(`${process.env.VUE_APP_SERVER_URL}/accounts/check_signup/`, {
          name: this.name,
          email: this.email + "@bookridge.com",
          password1: this.password1,
          password2: this.password2,
        })
        .then(() => {
          // console.log(res.data.result);
          // if (res.data.result == "success") {
          this.e1 = 2;
          // } else {
          // console.log(res.data);
          // swal(
          // `${res.data.error.password2}`,
          // "모든 값은 필수값입니다. 다시 한 번 입력값을 확인해주세요."
          // );
          // }
        })
        // .catch((err) => {
        //   console.log(err);
        // });
    },
    goToHome() {
      VueCookies.keys().forEach((cookie) => VueCookies.remove(cookie));
      this.$router.push("/");
    },
    onSelectImage(id) {
      // console.log(id);
      if (id == 1) {
        this.genre1 = !this.genre1;
      } else if (id == 2) {
        this.genre2 = !this.genre2;
      } else if (id == 3) {
        this.genre3 = !this.genre3;
      } else if (id == 4) {
        this.genre4 = !this.genre4;
      } else if (id == 5) {
        this.genre5 = !this.genre5;
      } else if (id == 6) {
        this.genre6 = !this.genre6;
      } else if (id == 7) {
        this.genre7 = !this.genre7;
      } else if (id == 8) {
        this.genre8 = !this.genre8;
      } else {
        this.genre9 = !this.genre9;
      }
      if (this.genres[id] == 0) {
        this.genres[id] = 1;
      } else {
        this.genres[id] = 0;
      }
    },
    checkEmail() {
      // axios 요청
      // console.log(this.email + "@bookridge.com");
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/accounts/check_email/`, {
          params: {
            email: this.email + "@bookridge.com",
          },
        })
        // true면 존재X
        .then((res) => {
          if (res.data.result) {
            this.isCheckedEmail = true;
            this.checkedEmail = this.email;
            swal("사용 가능한 이메일입니다.");
          } else {
            swal("이미 존재하는 이메일입니다.");
          }
          // console.log(res.data.object);
        })
        // .catch((err) => {
        //   console.log(err);
        // });
    },
    checkRules() {
      // console.log(document.getElementById("sample5_address").value);
      if (
        document.getElementById("sample5_address").value ===
        "'주소검색' 버튼을 눌러 주소를 검색해주세요."
      ) {
        this.addressRules = [false];
        this.checkbox = false;
        swal("주소를 입력해주세요.");
      } else {
        this.addressRules = [true];
      }
    },
    save(date) {
      this.$refs.menu.save(date);
    },
    submit() {
      // 소셜로그인 시 프로필 수정 요청으로 보내기
      if (VueCookies.get("social_id")) {
        axios
          .post(
            `${
              process.env.VUE_APP_SERVER_URL
            }/accounts/profile/${VueCookies.get("user_pk")}/`,
            {
              email: this.$route.params.email,
              birth: this.birth,
              name: this.$route.params.name,
              address: document.getElementById("sample5_address").value,
              latitude: parseFloat(document.getElementById("x").value),
              longitude: parseFloat(document.getElementById("y").value),
              gender: this.gender == "남자" ? 0 : 1,
              social: this.$route.params.social,
              social_id: VueCookies.get("social_id"),
              genres: this.genres.slice(1, 10),
            },
            {
              headers: {
                Authorization: VueCookies.get("jwt_token"),
              },
            }
          )
          .then((res) => {
            // console.log(res);
            VueCookies.set("user_gender", res.data.gender, "6h");
            // swal(`${res.data.name}님 북릿지에 오신걸 환영합니다.`);
            this.$router.push("/main");
            this.$router.go();
          })
          // .catch((err) => {
          //   console.log(err);
          // });
        // 일반회원가입 시 요청`
      } else {
        axios
          .post(`${process.env.VUE_APP_SERVER_URL}/accounts/signup/`, {
            name: this.name,
            email: this.email + "@bookridge.com",
            password1: this.password1,
            password2: this.password2,
            birth: this.birth,
            gender: this.gender == "남자" ? 0 : 1,
            address: document.getElementById("sample5_address").value,
            latitude: document.getElementById("x").value,
            longitude: document.getElementById("y").value,
            choice: this.choice,
            genres: this.genres.slice(1, 10),
          })
          .then(() => {
            // console.log(res);
            swal("회원가입을 정상적으로 마쳤습니다. 로그인해주세요!");
            this.$router.push("/");
          })
          // .catch((err) => {
          //   console.log(err);
          // });
      }
    },
    validate() {
      this.$refs.form1.validate();
    },
    validate2() {
      this.$refs.form2.validate();
    },
  },
  data() {
    return {
      genres: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      genre1: false,
      genre2: false,
      genre3: false,
      genre4: false,
      genre5: false,
      genre6: false,
      genre7: false,
      genre8: false,
      genre9: false,
      autoBooks: [],
      choice: [],
      selectedBooks: [],
      searchWord: null,
      checkbox1: false,
      items: [
        {
          title: "New Releases",
          img: "@/assets/img/philosophy.png",
        },
        {
          title: "Rock",
          img: "@/assets/img/religion.jpg",
        },
        {
          title: "Mellow Moods",
          img: "http://lorempixel.com/output/abstract-q-c-640-480-6.jpg",
        },
        {
          title: "New Releases",
          img: "http://lorempixel.com/output/nightlife-q-c-640-480-5.jpg",
        },
        {
          title: "Rock",
          img:
            "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2100&q=80",
        },
        {
          title: "Mellow Moods",
          img: "http://lorempixel.com/output/abstract-q-c-640-480-6.jpg",
        },
        {
          title: "New Releases",
          img: "http://lorempixel.com/output/nightlife-q-c-640-480-5.jpg",
        },
        {
          title: "Rock",
          img:
            "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2100&q=80",
        },
        {
          title: "Mellow Moods",
          img: "http://lorempixel.com/output/abstract-q-c-640-480-6.jpg",
        },
      ],
      transparent: "rgba(255, 255, 255, 0)",
      selectedImage: null,
      isCheckedEmail: true,
      checkedEmail: "정말말도안되는이메일",
      menu: false,
      isSocial: false,
      isLogin: false,
      e1: 1,

      modal: false,
      hide: false,
      locationX: "",
      locationY: "",

      dialogPolicy: false,

      checkbox: false,
      lazy1: false,
      lazy2: false,

      valid1: false,
      valid2: false,
      show1: false,
      show2: false,

      email: "",
      emailRules: [
        (v) => !!v || "아이디는 필수값입니다.",
        (v) => (v && v.length <= 15) || "15자 이내로 입력해주세요.",
      ],

      name: "",
      nameRules: [
        (v) => !!v || "이름은 필수값입니다.",
        (v) => (v && v.length <= 10) || "이름은 10자 이내로 입력해주세요.",
      ],
      password1: "",
      password1Rules: [
        (v) => !!v || "비밀번호는 필수값입니다.",
        (v) => (v && v.length >= 8) || "비밀번호는 8자 이상으로 입력해주세요.",
      ],
      password2: "",
      password2Rules: [
        (v) => !!v || "비밀번호는 필수값입니다.",
        (v) => this.password1 == v || "잘못된 비밀번호입니다.",
        (v) => (v && v.length >= 8) || "비밀번호는 8자 이상으로 입력해주세요.",
      ],

      gender: null,
      genders: ["남자", "여자"],
      genderRules: [(v) => !!v || "성별은 필수값입니다."],

      birth: null,
      birthdayRules: [(v) => !!v || "생년월일은 필수값입니다."],

      address: "'주소검색' 버튼을 눌러 주소를 검색해주세요.",
      addressRules: [false],

      agreeRules: [(v) => !!v || "약관동의는 필수입니다."],
    };
  },
};
</script>
<style scoped>
.vertical {
  vertical-align: middle;
}

.bookimage {
  width: 200px;
  height: 300px;
  margin: 0px auto;
}

.book-image {
  width: 50px;
  height: 50px;
  margin: 0px auto;
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
.card .imgBx,
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
body {
  background-color: #212121;
}

/*  */
.main-color {
  background-color: rgba(0, 150, 136, 0.7);
}
.text-black {
  color: black;
}
.basic {
  transition: opacity 0.4s ease-in-out;
}

.on-hover {
  opacity: 0.6;
}

.card-img {
  width: 250px;
  height: 250px;
}
.address-btn {
  font-size: 15px;
  border-radius: 5px;
  box-shadow: 0.5px 0.5px 0.5px 0.5px #bdbdbd;
  background-color: #4caf50;
  border: none;
  color: white;
  padding: 6px 14px;

  margin: 4px 2px;
  cursor: pointer;
}
.address-btn:hover {
  opacity: 0.9;
}
.nohover {
  cursor: default;
}
.text-green {
  color: green;
}
.text-red {
  color: red;
}
.v-responsive__content {
  opacity: 100;
}
.tma {
  width: 70%;
}
</style>