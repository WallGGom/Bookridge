<template>
  <div id="main d-flex flex-row" class="my-5 bg">
    <transition name="fade">
      <div id="element" class="loading" v-show="isLoading">
        <div class="fa-3x"><i class="fas fa-spinner fa-spin"></i> Loading</div>
      </div>
    </transition>
    <v-container class="mx-auto" style="min-width: 1000px">
      <v-tabs vertical color="white">
        <v-container class="pt-0">
          <v-card class="mx-auto text-center pt-5" width="250">
            <v-img
              :src="profile_url"
              class="rounded-circle mx-auto"
              width="50%"
              height="50%"
            >
            </v-img>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-subtitle
                  width="250"
                  v-show="name"
                  style="
                    font-family: HangeulNuri-Bold;
                    color: black;
                    font-size: large;
                  "
                  >{{ this.name }}님의 프로필</v-list-item-subtitle
                >
              </v-list-item-content>
            </v-list-item>
            <v-tab
              class="d-flex justify-content-start"
              @click="toTop"
              style="font-family: HangeulNuri-Bold; color: black"
            >
              <v-icon left style="color: black">mdi-account</v-icon>상세 프로필
            </v-tab>
            <v-tab
              class="d-flex justify-content-start"
              @click="toTop"
              v-if="!social"
              style="font-family: HangeulNuri-Bold; color: black"
            >
              <v-icon left style="color: black">mdi-account-lock</v-icon
              >비밀번호 수정
            </v-tab>
            <v-tab
              class="d-flex justify-content-start"
              @click="toTop"
              style="font-family: HangeulNuri-Bold; color: black"
            >
              <v-icon left style="color: black">mdi-account-remove</v-icon>회원
              탈퇴
            </v-tab>
          </v-card>
        </v-container>
        <!-- 상세 프로필 -->
        <v-tab-item>
          <v-card height="100%" color>
            <v-card-text>
              <v-container class="bv-example-row pl-5">
                <v-row class="my-5 d-flex justify-content-center">
                  <h2 style="font-family: HangeulNuri-Bold">프로필 정보</h2>
                </v-row>
                <v-row class="d-flex justify-content-center">
                  <v-btn
                    @click="updateNow = true"
                    class="ma-2 mt-3 mb-5"
                    outlined
                    color="#009688"
                    v-show="!updateNow && !!social"
                    style="font-family: HangeulNuri-Bold"
                    >프로필 수정</v-btn
                  >
                  <v-dialog
                    v-model="dialogPw"
                    @keydown.esc="closeDialog"
                    persistent
                    width="400"
                    height="270"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        class="ma-2 mt-3 mb-5"
                        outlined
                        color="#009688"
                        v-show="!updateNow && !social"
                        v-bind="attrs"
                        v-on="on"
                        style="font-family: HangeulNuri-Bold"
                        >프로필 수정</v-btn
                      >
                    </template>
                    <v-card width="400" height="270">
                      <v-card-title
                        class="headline main-color justify-content-center text-white"
                        >프로필 수정</v-card-title
                      >
                      <v-card-text class="p-3 mt-5">
                        <h6 style="font-family: HangeulNuri-Bold">
                          프로필 수정을 위해 비밀번호를 입력해주세요.
                        </h6>
                        <v-text-field
                          v-model="password"
                          color="#009688"
                          label="비밀번호를 입력해주세요."
                          type="password"
                          clearable
                        ></v-text-field>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                          color="success"
                          text
                          @click="checkPassword(0), (dialogPw = false)"
                          style="font-family: HangeulNuri-Bold"
                          >확인</v-btn
                        >
                        <v-btn
                          color="error"
                          text
                          @click="closeDialog"
                          style="font-family: HangeulNuri-Bold"
                          >취소</v-btn
                        >
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-row>
                <v-list two-line class="text-center">
                  <!-- <v-subheader inset>상세 프로필</v-subheader> -->
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1" class="py-0">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-tag-text-outline</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3" class="py-0">
                        <v-list-item-content>
                          <v-list-item-title
                            style="font-family: HangeulNuri-Bold"
                            >이름</v-list-item-title
                          >
                          <v-list-item-subtitle
                            v-show="updateNow"
                            style="font-family: HangeulNuri-Bold"
                            >필수정보입니다.</v-list-item-subtitle
                          >
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5" class="py-0">
                        <v-list-item-content>
                          <h6
                            v-show="!updateNow"
                            style="font-family: HangeulNuri-Bold"
                          >
                            {{ newName }}
                          </h6>
                          <v-form
                            ref="form1"
                            v-model="validName"
                            class="form-width"
                          >
                            <v-text-field
                              :rules="nameRules"
                              v-show="updateNow"
                              v-model="newName"
                              clearable
                              label="이름을 입력해주세요."
                              style="font-family: HangeulNuri-Bold"
                              outlined
                            ></v-text-field>
                          </v-form>
                        </v-list-item-content>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1" class="px-0">
                        <v-avatar size="48" class="pl-5">
                          <v-icon class="mb-5">mdi-face</v-icon>
                          <v-icon class="pr-5">mdi-face-woman</v-icon>
                        </v-avatar>
                      </v-col>
                      <v-col cols="3">
                        <v-list-item-content>
                          <v-list-item-title
                            style="font-family: HangeulNuri-Bold"
                            >성별</v-list-item-title
                          >
                          <v-list-item-subtitle
                            v-show="updateNow"
                            style="font-family: HangeulNuri-Bold"
                            >필수정보입니다.</v-list-item-subtitle
                          >
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5">
                        <v-list-item-content>
                          <h6
                            v-show="!updateNow"
                            style="font-family: HangeulNuri-Bold"
                          >
                            {{ newGender }}
                          </h6>
                          <v-select
                            style="font-family: HangeulNuri-Bold"
                            v-show="updateNow"
                            v-model="newGender"
                            :items="genders"
                            :rules="[(v) => !!v || '성별을 입력해주세요.']"
                            label="성별"
                            required
                          ></v-select>
                        </v-list-item-content>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-cake-variant</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3" class="mt-1">
                        <v-list-item-content>
                          <v-list-item-title
                            style="font-family: HangeulNuri-Bold"
                            >생년월일</v-list-item-title
                          >
                          <v-list-item-subtitle
                            v-show="updateNow"
                            style="font-family: HangeulNuri-Bold"
                            >필수정보입니다.</v-list-item-subtitle
                          >
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5" class="mt-1">
                        <v-list-item-content>
                          <h6
                            v-show="!updateNow"
                            style="font-family: HangeulNuri-Bold"
                          >
                            {{ newBirth }}
                          </h6>
                          <v-menu
                            ref="menu"
                            v-model="menu"
                            :close-on-content-click="false"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                style="font-family: HangeulNuri-Bold"
                                v-show="updateNow"
                                v-model="newBirth"
                                label="생년월일을 입력해주세요."
                                readonly
                                v-bind="attrs"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-date-picker
                              style="font-family: HangeulNuri-Bold"
                              v-show="updateNow"
                              ref="picker"
                              v-model="newBirth"
                              :max="new Date().toISOString().substr(0, 10)"
                              min="1950-01-01"
                              @change="save"
                              locale="south-korea"
                              color="#009688"
                            ></v-date-picker>
                          </v-menu>
                        </v-list-item-content>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-map-marker</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3">
                        <v-list-item-content>
                          <v-list-item-title
                            style="font-family: HangeulNuri-Bold"
                            >주소</v-list-item-title
                          >
                          <v-list-item-subtitle
                            v-show="updateNow"
                            style="font-family: HangeulNuri-Bold"
                            >필수정보입니다.</v-list-item-subtitle
                          >
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5">
                        <v-list-item-content>
                          <h6
                            v-show="!updateNow"
                            style="font-family: HangeulNuri-Bold"
                          >
                            {{ address }}
                          </h6>
                          <v-text-field
                            v-show="updateNow"
                            type="text"
                            id="sample5_address"
                            placeholder="주소를 검색해주세요."
                            disabled
                            style="font-family: HangeulNuri-Bold"
                          ></v-text-field>
                          <!-- longitude -->
                          <v-text-field
                            type="text"
                            v-show="hide"
                            id="x"
                            placeholder="주소"
                            disabled
                          ></v-text-field>
                          <!-- latitude -->
                          <v-text-field
                            type="text"
                            v-show="hide"
                            id="y"
                            placeholder="주소"
                            disabled
                          ></v-text-field>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="2">
                        <v-list-item-content>
                          <input
                            v-show="updateNow"
                            type="button"
                            onclick="sample5_execDaumPostcode()"
                            value="주소 검색"
                            class="mt-5 mr-3 address-btn"
                            style="font-family: HangeulNuri-Bold"
                            uk-tooltip="버튼을 클릭해주세요."
                          />
                        </v-list-item-content>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1" class="pt-3 pb-0">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-tag-text-outline</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3" class="pt-3 pb-0">
                        <v-list-item-content>
                          <v-list-item-title
                            style="font-family: HangeulNuri-Bold"
                            >선호 장르</v-list-item-title
                          >
                          <v-list-item-subtitle
                            v-show="updateNow"
                            style="font-family: HangeulNuri-Bold"
                            >선택사항입니다.</v-list-item-subtitle
                          >
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5" v-show="!updateNow" class="pt-3 pb-0">
                        <v-list-item-content class="pt-0">
                          <h6
                            style="font-family: HangeulNuri-Bold"
                            class="mt-3 text-center"
                          >
                            <span v-if="newCheckbox1" class="mr-1">철학</span>
                            <span v-if="newCheckbox2" class="mr-1">종교</span>
                            <span v-if="newCheckbox3" class="mr-1"
                              >사회과학</span
                            >
                            <span v-if="newCheckbox4" class="mr-1"
                              >순수과학</span
                            >
                            <span v-if="newCheckbox5" class="mr-1"
                              >기술과학</span
                            >
                            <span v-if="newCheckbox6" class="mr-1">예술</span>
                            <span v-if="newCheckbox7" class="mr-1">언어</span>
                            <span v-if="newCheckbox8" class="mr-1">문학</span>
                            <span v-if="newCheckbox9" class="mr-1">역사</span>
                          </h6>
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="8" v-show="updateNow" class="pt-3 pb-0">
                        <v-list-item-content class="pt-0">
                          <v-container class="p-0">
                            <v-row class="ml-1">
                              <v-col class="pt-0">
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox1"
                                  label="철학"
                                ></v-checkbox>
                              </v-col>
                              <v-col class="pt-0">
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox2"
                                  label="종교"
                                ></v-checkbox>
                              </v-col>
                              <v-col class="pt-0">
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox3"
                                  label="사회과학"
                                ></v-checkbox>
                              </v-col>
                            </v-row>
                            <v-row class="ml-1">
                              <v-col>
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox4"
                                  label="순수과학"
                                ></v-checkbox>
                              </v-col>

                              <v-col>
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox5"
                                  label="기술과학"
                                ></v-checkbox>
                              </v-col>
                              <v-col>
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox6"
                                  label="예술"
                                ></v-checkbox
                              ></v-col>
                            </v-row>
                            <v-row class="ml-1">
                              <v-col>
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox7"
                                  label="언어"
                                ></v-checkbox
                              ></v-col>
                              <v-col>
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox8"
                                  label="문학"
                                ></v-checkbox>
                              </v-col>
                              <v-col>
                                <v-checkbox
                                  color="success"
                                  class="main-font"
                                  v-model="newCheckbox9"
                                  label="역사"
                                ></v-checkbox>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-list-item-content>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-row>
                      <v-col cols="1">
                        <v-list-item-avatar>
                          <v-icon class="mb-5">mdi-account-circle</v-icon>
                        </v-list-item-avatar>
                      </v-col>
                      <v-col cols="3">
                        <v-list-item-content>
                          <v-list-item-title
                            style="font-family: HangeulNuri-Bold"
                            >아바타</v-list-item-title
                          >
                          <v-list-item-subtitle
                            v-show="updateNow"
                            style="font-family: HangeulNuri-Bold"
                            >선택사항입니다.</v-list-item-subtitle
                          >
                        </v-list-item-content>
                      </v-col>
                      <v-col cols="5" v-if="!updateNow">
                        <v-img
                          :src="profile_url"
                          class="rounded-circle mx-auto"
                          width="50%"
                          height="100%"
                        >
                        </v-img>
                      </v-col>
                      <v-col cols="7">
                        <v-list-item-content>
                          <v-row v-show="updateNow && !isSelected">
                            <v-col
                              v-for="(ava, i) in avatars"
                              width="70%"
                              height="70%"
                              :key="i"
                              cols="3"
                            >
                              <v-row>
                                <v-img
                                  :src="`https://joeschmoe.io/api/v1/${avatars[i]}`"
                                  class="rounded-circle"
                                  width="100%"
                                  height="100%"
                                  @click="choiceAvatar(i)"
                                >
                                </v-img
                              ></v-row>
                            </v-col>
                          </v-row>
                          <v-row v-show="updateNow && isSelected">
                            <v-img
                              :src="`https://joeschmoe.io/api/v1/${avatars[selectI]}`"
                              class="rounded-circle"
                              width="100%"
                              height="100%"
                            >
                            </v-img
                            ><v-row
                              ><v-btn
                                uk-tooltip="선택 취소"
                                text
                                class="mx-auto"
                                @click="choiceAvatar(selectI)"
                                color="secondary"
                                style="font-family: HangeulNuri-Bold"
                                >취소</v-btn
                              ></v-row
                            >
                          </v-row>
                        </v-list-item-content>
                      </v-col>
                    </v-row>
                  </v-list-item>
                  <v-divider></v-divider>
                </v-list>
                <div class="text-center w-100" v-show="updateNow">
                  <v-btn
                    text
                    :disabled="!validName"
                    color="success"
                    @click="saveProfile"
                    style="font-family: HangeulNuri-Bold"
                    >프로필 저장</v-btn
                  >
                  <v-btn
                    text
                    outlined
                    color="error"
                    dark
                    @click="cancelProfile()"
                    class="mx-1"
                    style="font-family: HangeulNuri-Bold"
                    >취소</v-btn
                  >
                </div>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <!-- 비밀번호 수정 -->
        <v-tab-item v-if="!social">
          <v-card height="100%" color>
            <v-card-text>
              <v-container class="bv-example-row pl-5">
                <v-row>
                  <v-col cols="9">
                    <h2 style="font-family: HangeulNuri-Bold">비밀번호 수정</h2>
                  </v-col>
                  <v-col cols="3" class="text-right">
                    <v-dialog
                      v-model="dialogChangePw"
                      @keydown.esc="dialogChangePw = false"
                      persistent
                      width="450"
                      height="280"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          class="ma-2"
                          outlined
                          color="#009688"
                          v-bind="attrs"
                          v-on="on"
                          v-show="!updatePwNow && !social"
                          style="font-family: HangeulNuri-Bold"
                          >비밀번호 수정</v-btn
                        >
                      </template>
                      <v-card width="450" height="280">
                        <v-card-title
                          class="headline main-color justify-content-center text-white"
                          >비밀번호 수정</v-card-title
                        >
                        <v-card-text class="p-3 mt-5">
                          <h6 style="font-family: HangeulNuri-Bold">
                            비밀번호 수정을 위해 현재 비밀번호를 입력해주세요.
                          </h6>
                          <v-text-field
                            v-model="password"
                            color="#009688"
                            label="비밀번호를 입력해주세요."
                            type="password"
                            clearable
                          ></v-text-field>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                            color="success"
                            text
                            @click="checkPassword(1), (dialogChangePw = false)"
                            style="font-family: HangeulNuri-Bold"
                            >확인</v-btn
                          >
                          <v-btn
                            color="error"
                            text
                            @click="(dialogChangePw = false), (password = '')"
                            style="font-family: HangeulNuri-Bold"
                            >취소</v-btn
                          >
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-col>
                </v-row>
                <div class="my-5">
                  <v-sheet
                    color
                    :outlined="true"
                    class="py-5"
                    v-show="!updatePwNow"
                  >
                    <h5
                      class="px-5 mb-5 text-blue"
                      style="font-family: HangeulNuri-Bold"
                    >
                      비밀번호 수정 안내
                    </h5>
                    <h6 class="px-5" style="font-family: HangeulNuri-Bold">
                      비밀번호 수정을 원하시면 "비밀번호 수정" 버튼을 클릭하여
                      비밀번호를 인증해주세요.
                    </h6>
                  </v-sheet>
                </div>
                <v-list two-line subheader v-show="updatePwNow">
                  <v-card>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col
                            cols="3"
                            class="mt-5"
                            style="font-family: HangeulNuri-Bold"
                            >새 비밀번호1</v-col
                          >
                          <v-col cols="9">
                            <v-text-field
                              v-model="newPassword1"
                              color="#009688"
                              :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                              :rules="rulesPw"
                              :type="show1 ? 'text' : 'password'"
                              label="변경할 비밀번호를 입력해주세요."
                              hint="최소 8자 이상으로 비밀번호를 설정해주세요."
                              counter
                              @click:append="show1 = !show1"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col
                            cols="3"
                            class="mt-5"
                            style="font-family: HangeulNuri-Bold"
                            >새 비밀번호2</v-col
                          >
                          <v-col cols="9">
                            <v-text-field
                              color="#009688"
                              v-model="newPassword2"
                              :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                              :rules="rulesPw"
                              :type="show2 ? 'text' : 'password'"
                              label="한 번 더 입력해주세요."
                              hint="최소 8자 이상으로 비밀번호를 설정해주세요."
                              counter
                              @click:append="show2 = !show2"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                  </v-card>
                  <div class="d-flex justify-content-center my-5">
                    <v-btn
                      style="font-family: HangeulNuri-Bold"
                      class="ma-2"
                      outlined
                      color="success"
                      text
                      @click="updatePassword"
                      v-if="
                        newPassword1.length > 7 &&
                        newPassword2.length > 7 &&
                        newPassword1 === newPassword2
                      "
                      >저장</v-btn
                    >
                    <v-btn
                      color="success"
                      class="ma-2"
                      outlined
                      disabled
                      v-else
                      style="font-family: HangeulNuri-Bold"
                      >저장</v-btn
                    >
                    <v-btn
                      @click="cancelUpdatePassword"
                      class="ma-2"
                      outlined
                      color="error"
                      style="font-family: HangeulNuri-Bold"
                      >취소</v-btn
                    >
                  </div>
                </v-list>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>
        <!-- 회원 탈퇴 -->
        <v-tab-item>
          <v-card height="100%">
            <v-card-text>
              <v-container class="bv-example-row pl-5">
                <v-row class="d-flex justify-content-center">
                  <h2 style="font-family: HangeulNuri-Bold">회원 탈퇴</h2>
                </v-row>
                <div class="text-center my-5 table-cell">
                  <v-sheet
                    color="grey lighten-2"
                    class="px-3 py-5 vertical"
                    min-height="200px"
                  >
                    <h4 class="mt-5 pt-5" style="font-family: HangeulNuri-Bold">
                      {{ name }}님의 {{ email }} 계정을 탈퇴합니다.
                    </h4>
                    <h4 class="mt-5" style="font-family: HangeulNuri-Bold">
                      회원 탈퇴가 완료되면 회원님의 개인정보는 즉시 삭제됩니다.
                    </h4>
                  </v-sheet>
                </div>
                <div class="my-5" style="font-family: HangeulNuri-Bold">
                  <v-sheet color :outlined="true" class="py-5">
                    <h5
                      class="pl-5 mb-5 text-blue"
                      style="font-family: HangeulNuri-Bold"
                    >
                      탈퇴 전 주의사항
                    </h5>
                    <p class="pl-5">1. 삭제된 데이터는 복구할 수 없습니다.</p>
                    <p class="pl-5">
                      2. 해당 아이디로 작성된 게시물은 삭제되지 않습니다.
                    </p>
                  </v-sheet>
                </div>
                <div class="text-center">
                  <v-dialog
                    width="500"
                    v-model="dialogDeleteAccount"
                    @keydown.esc="dialogDeleteAccount = false"
                    persistent
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        class="ma-2"
                        outlined
                        color="#009688"
                        v-bind="attrs"
                        v-on="on"
                        style="font-family: HangeulNuri-Bold"
                        >회원 탈퇴</v-btn
                      >
                    </template>
                    <v-card width="500" min-height="300">
                      <v-card-title
                        class="headline main-color justify-content-center text-white"
                        style="
                          font-family: HangeulNuri-Bold;
                          font-size: x-large;
                        "
                        >회원 탈퇴</v-card-title
                      >
                      <v-card-text class="p-3 mt-5">
                        <h5
                          style="
                            font-family: HangeulNuri-Bold;
                            font-size: large;
                          "
                        >
                          정말 탈퇴를 진행하시겠습니까?
                        </h5>
                        <span
                          v-show="!social"
                          style="
                            font-family: HangeulNuri-Bold;
                            font-size: large;
                          "
                          >회원 탈퇴 희망시 비밀번호를 입력해주세요.</span
                        >
                        <span
                          v-show="!!social"
                          style="
                            font-family: HangeulNuri-Bold;
                            font-size: large;
                          "
                          >회원 탈퇴 희망시 '확인' 버튼을 클릭해주세요.</span
                        >
                        <br />
                        <br />
                        <span
                          class="mb-5"
                          style="
                            font-family: HangeulNuri-Bold;
                            font-size: small;
                            color: #ff8a80;
                          "
                          >주의) 한 번 진행하면 되돌릴 수 없습니다.</span
                        >
                        <v-text-field
                          v-show="!social"
                          v-model="password"
                          color="#009688"
                          label="비밀번호를 입력해주세요."
                          type="password"
                          clearable
                        ></v-text-field>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <!-- !!!!!!!!!!!!! -->
                        <v-btn
                          v-if="!social"
                          color="success"
                          text
                          @click="
                            checkPassword(2), (dialogDeleteAccount = false)
                          "
                          style="font-family: HangeulNuri-Bold"
                          >확인</v-btn
                        >
                        <v-btn
                          v-else
                          color="success"
                          text
                          @click="
                            deleteAccount(), (dialogDeleteAccount = false)
                          "
                          style="font-family: HangeulNuri-Bold"
                          >확인</v-btn
                        >
                        <v-btn
                          color="error"
                          text
                          @click="
                            (dialogDeleteAccount = false), (password = '')
                          "
                          style="font-family: HangeulNuri-Bold"
                          >취소</v-btn
                        >
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </div>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-container>
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
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "Profile",
  components: {},

  beforeRouteEnter(to, from, next) {
    if (!VueCookies.get("jwt_token")) {
      next("/");
      // swal("잘못된 접근입니다.1");
    } else {
      next();
    }
  },

  data() {
    return {
      oldGenres: [],
      genres: [],
      checkbox1: false,
      newCheckbox1: false,

      checkbox2: false,
      newCheckbox2: false,

      checkbox3: false,
      newCheckbox3: false,

      checkbox4: false,
      newCheckbox4: false,

      checkbox5: false,
      newCheckbox5: false,

      checkbox6: false,
      newCheckbox6: false,

      checkbox7: false,
      newCheckbox7: false,

      checkbox8: false,
      newCheckbox8: false,

      checkbox9: false,
      newCheckbox9: false,

      isSelected: false,
      selectI: 0,
      profile: null,
      dialog: false,

      date: new Date().toISOString().substr(0, 10),

      validName: true,
      nameRules: [
        (v) => !!v || "이름은 필수값입니다.",
        (v) => (v && v.length <= 10) || "이름은 10자 이내로 입력해주세요.",
      ],

      isLogin: true,

      show1: false,
      show2: false,

      rulesPw: [
        (v) => !!v || "비밀번호는 필수값입니다.",
        (v) => (v && v.length >= 8) || "비밀번호는 8자 이상으로 입력해주세요.",
      ],

      genders: ["남자", "여자"],

      // 개인정보
      name: "", // 닉네임
      newName: "", // 새로운 닉네임
      profile_url: "",

      email: null,

      birth: null,
      newBirth: null,
      menu: false,

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

      // dialog 모음

      // 프로필 수정시 비밀번호 물어보는 dialog
      dialogPw: false,
      // 개인보안 dialog
      dialogSecurityAccount: false,
      // 비밀번호 수정 dialog
      dialogChangePw: false,
      // 회원탈퇴 dialog
      dialogDeleteAccount: false,

      // 수정 여부
      updateNow: false,
      updatePwNow: false,

      // 스크롤
      fab: false,

      // 탭
      tab: null,

      // 기본정보 값
      isLoading: false,

      avatars: [
        "jazebelle",
        "jana",
        "jed",
        "jaqueline",
        "jenni",
        "julie",
        "jia",
        "jerry",
        "jean",
        "jude",
        "jake",
        "jane",
        "jon",
        "jack",
        "jacques",
        "joe",
        "james",
        "jordan",
        "jess",
        "jeri",
        "jeane",
        "jabala",
        "josh",
        "jocelyn",
        "jai",
        "josephine",
        "jodi",
        "jolee",
      ],
    };
  },
  created() {
    // 소셜 회원가입 미완료할 경우
    if (VueCookies.get("user_gender") == 2) {
      swal("잘못된 접근입니다.", "회원가입이 완료되지 않았습니다.");
      this.$router.push("/signup");
    }

    // this.isLoading = true;
    this.isLogin = VueCookies.get("jwt_token") ? true : false;

    // 프로필 정보 가져오기
    axios
      .get(
        `${process.env.VUE_APP_SERVER_URL}/accounts/profile/${VueCookies.get(
          "user_pk"
        )}/`,
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
        this.newName = res.data.name;

        this.profile_url = res.data.profile_url;

        this.profile = res.data.privacy;

        this.email = res.data.email;

        this.gender = res.data.gender == 0 ? "남자" : "여자";
        this.newGender = this.gender;
        this.oldGenres = res.data.genres;
        this.birth = res.data.birth;
        this.newBirth = this.birth;
        this.checkbox1 = res.data.genres[0];
        this.newCheckbox1 = res.data.genres[0];
        this.checkbox2 = res.data.genres[1];
        this.newCheckbox2 = res.data.genres[1];
        this.checkbox3 = res.data.genres[2];
        this.newCheckbox3 = res.data.genres[2];
        this.checkbox4 = res.data.genres[3];
        this.newCheckbox4 = res.data.genres[3];
        this.checkbox5 = res.data.genres[4];
        this.newCheckbox5 = res.data.genres[4];
        this.checkbox6 = res.data.genres[5];
        this.newCheckbox6 = res.data.genres[5];
        this.checkbox7 = res.data.genres[6];
        this.newCheckbox7 = res.data.genres[6];
        this.checkbox8 = res.data.genres[7];
        this.newCheckbox8 = res.data.genres[7];
        this.checkbox9 = res.data.genres[8];
        this.newCheckbox9 = res.data.genres[8];

        document.getElementById("sample5_address").value = res.data.address;
        this.address = res.data.address;

        document.getElementById("x").value = res.data.latitude;
        this.latitude = res.data.latitude;
        document.getElementById("y").value = res.data.longitude;
        this.longitude = res.data.longitude;

        this.social = res.data.social;
      });
    // .catch((err) => {
    //   console.log(err);
    // });
  },
  watch: {
    menu(val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = "YEAR"));
    },
  },

  methods: {
    // 아바타 선택
    choiceAvatar(i) {
      if (this.isSelected) {
        this.selectI = this.profile;
      } else {
        this.selectI = i;
      }
      this.isSelected = !this.isSelected;
    },
    // 날짜 저장
    save(date) {
      this.$refs.menu.save(date);
    },
    // 회원탈퇴
    deleteAccount() {
      axios
        .delete(`${process.env.VUE_APP_SERVER_URL}/accounts/unlink/`, {
          // social_id: VueCookies.get("social_id"),
          headers: { Authorization: VueCookies.get("jwt_token") },
        })
        .then(() => {
          VueCookies.keys().forEach((cookie) => VueCookies.remove(cookie));
          // console.log(res);
          swal("정상적으로 회원탈퇴 되었습니다.");
          this.$router.push("/");
          this.$router.go();
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },

    // 모달 닫는 부분
    closeDialog() {
      this.dialogPw = false;
      this.dialogChangePw = false;
      this.password = "";
      this.newPassword1 = "";
      this.newPassword2 = "";
    },

    // 비밀번호 일치여부 확인 후 상태변화
    // flag 0 = 프로필 수정 | flag 1 = 비밀번호 수정 | flag 2 = 회원 탈퇴
    checkPassword(flag) {
      axios
        .get(
          `${process.env.VUE_APP_SERVER_URL}/accounts/password/${VueCookies.get(
            "user_pk"
          )}/`,
          {
            params: {
              password: this.password,
            },
            headers: { Authorization: VueCookies.get("jwt_token") },
          }
        )
        .then((res) => {
          if (res.data.result) {
            if (flag == 0) {
              this.updateNow = true;
              this.password = "";
            } else if (flag == 1) {
              this.updatePwNow = true;
              this.nowPassword = this.password;
              this.password = "";
            } else if (flag == 2) {
              this.password = "";
              this.deleteAccount();
            }
          } else {
            this.password = "";
            swal("비밀번호가 일치하지 않습니다. 다시 시도해주세요.");
          }
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },
    // 비밀번호 수정
    updatePassword() {
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/accounts/password/${VueCookies.get(
            "user_pk"
          )}/`,
          {
            password: this.nowPassword,
            password1: this.newPassword1,
            password2: this.newPassword2,
          },
          {
            headers: {
              Authorization: VueCookies.get("jwt_token"),
            },
          }
        )
        .then(() => {
          swal("비밀번호가 변경되었습니다.");
          this.updatePwNow = false;
          this.password = "";
          this.newPassword1 = "";
          this.newPassword2 = "";
        });
      // .catch((err) => {
      //   console.log(err);
      // });
    },

    cancelUpdatePassword() {
      this.updatePwNow = false;
      swal("비밀번호 변경이 취소되었습니다.");
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

    // 프로필 저장
    saveProfile() {
      axios
        .post(
          `${process.env.VUE_APP_SERVER_URL}/accounts/profile/${VueCookies.get(
            "user_pk"
          )}/`,
          {
            email: this.email,
            birth: this.newBirth,
            name: this.newName,
            address: document.getElementById("sample5_address").value,
            latitude: document.getElementById("x").value,
            longitude: document.getElementById("y").value,
            gender: this.newGender == "남자" ? 0 : 1,
            social: this.social,
            social_id: VueCookies.get("social_id"),
            profile: this.selectI,
            genres: [
              this.newCheckbox1,
              this.newCheckbox2,
              this.newCheckbox3,
              this.newCheckbox4,
              this.newCheckbox5,
              this.newCheckbox6,
              this.newCheckbox7,
              this.newCheckbox8,
              this.newCheckbox9,
            ],
          },
          {
            headers: {
              Authorization: VueCookies.get("jwt_token"),
            },
          }
        )
        .then((res) => {
          (this.birth = this.newBirth),
            (this.name = this.newName),
            (this.address = document.getElementById("sample5_address").value),
            (this.latitude = document.getElementById("x").value),
            (this.longitude = document.getElementById("y").value),
            (this.gender = this.newGender == "남자" ? 0 : 1);
          this.profile_url = res.data.profile_url;
          if (this.genres != this.oldGenres) { sessionStorage.clear(); }
          // console.log("수정 후 데이터");
          // console.log(res);
        });
      swal("성공적으로 저장되었습니다.");
      this.updateNow = false;
      // this.$router.go();
    },
    // 프로필 수정 취소
    cancelProfile() {
      this.updateNow = !this.updateNow;
      //   this.profileImgUrl = this.profileImg;
      this.newName = this.name;
      this.newBirth = this.birth;
      document.getElementById("sample5_address").value = this.address;
      document.getElementById("x").value = this.latitude;
      document.getElementById("y").value = this.longitude;
      this.newCheckbox1 = this.checkbox1;
      this.newCheckbox2 = this.checkbox2;
      this.newCheckbox3 = this.checkbox3;
      this.newCheckbox4 = this.checkbox4;
      this.newCheckbox5 = this.checkbox5;
      this.newCheckbox6 = this.checkbox6;
      this.newCheckbox7 = this.checkbox7;
      this.newCheckbox8 = this.checkbox8;
      this.newCheckbox9 = this.checkbox9;
      swal("프로필 수정이 취소되었습니다.");
      // this.$router.go();
    },

    // 개인보안 수정 취소
    cancelSecurity() {
      this.updatePwNow = false;
      swal("취소되었습니다.");
    },
  },
};
</script>

<style scoped>
.main-font {
  font-family: "HangeulNuri-Bold";
}
/* 내가 작성한 CSS */
.text-white {
  color: white;
}

.vertical {
  vertical-align: middle;
}

.v-tabs-slider {
  background-color: white;
}
.address-btn {
  font-size: 15px;
  width: 25px;
  color: green;
  background-color: white;

  padding: 6px 14px;

  margin: 4px 2px;
  cursor: pointer;
}
.address-btn:hover {
  opacity: 0.7;
  background-color: rgb(239, 247, 229);
  /* box-shadow: 0.5px 0.5px 0.5px 0.5px green; */
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
  font-family: "InfinitySans-RegularA1";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/InfinitySans-RegularA1.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}

.v-card__title.headline.main-color.justify-content-center.text-white {
  font-family: "InfinitySans-RegularA1" !important;
  background-color: #4db6ac;
}
</style>