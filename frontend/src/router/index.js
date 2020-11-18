import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Main from '../views/Main.vue'

// Oauth
import OauthGoogle from '../views/oauth/OauthGoogle.vue'
import OauthKakao from '../views/oauth/OauthKakao.vue'

// accounts
import Signup from '../views/accounts/Signup.vue'
import Profile from '../views/accounts/Profile.vue'
import Activity from '../views/accounts/Activity.vue'

// community
import Community from '../views/community/Community.vue'
import ReviewDetail from '../views/community/ReviewDetail.vue'

// search
import Search from '../views/search/Search.vue'
import Search2 from '../views/search/Search2.vue'

//form
import ReviewForm from '../views/form/ReviewForm.vue'
import PhraseForm from '../views/form/PhraseForm.vue'

//detail
import BookDetail from '../views/detail/BookDetail.vue'

// analyze
import Analyze from '../views/analyze/Analyze.vue'
import Chart from '../views/analyze/Chart.vue'

//algorithm
import Algo from '../views/Algo.vue'


Vue.use(VueRouter)


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    props: true,
  },
  {
    path: '/profile/',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/activity/:pk',
    name: 'Activity',
    component: Activity,
    props: true,
  },
  {
    path: '/reviewdetail/:pk',
    name: 'ReviewDetail',
    component: ReviewDetail,
    props: true,
  },
  {
    path: '/main',
    name: 'Main',
    component: Main,
  },
  {
    path: '/algo/:pk',
    name: 'Algo',
    component: Algo,
    props: true,
  },
  {
    path: '/community',
    name: 'Community',
    component: Community,
  },
  {
    path: '/search/:search_word/:search_type',
    name: 'Search',
    component: Search,
    props: true,
  },
  {
    path: '/search2',
    name: 'Search2',
    component: Search2,
  },
  {
    path: '/reviewform',
    name: 'ReviewForm',
    component: ReviewForm,
  },
  {
    path: '/phraseform',
    name: 'PhraseForm',
    component: PhraseForm
  },
  {
    path: '/bookdetail/:pk',
    name: 'BookDetail',
    component: BookDetail,
    props: true,
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: Analyze
  },
  {
    path: '/chart',
    name: 'Chart',
    component: Chart
  },
  {
    path: '/oauthgoogle',
    name: 'OauthGoogle',
    component: OauthGoogle
  },
  {
    path: '/oauthkakao',
    name: 'OauthKakao',
    component: OauthKakao
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
