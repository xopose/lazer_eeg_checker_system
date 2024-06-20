<script setup async>

import {useAPI, USER_ID} from "@/hooks/useAPI";
import {useRouter} from "vue-router";
import {onMounted, ref} from "vue";

const Router = useRouter()
const isLoading = ref(true)
const {getUserById} = useAPI()
const user = ref(null)
const {setDoneResearch} = useAPI()
const isShowSnackbar = ref(false)

const id = Number(localStorage.getItem(USER_ID))
if (!id)
  Router.push("/")


onMounted(async () => {
  user.value = await getUserById(id)
  isLoading.value = false
  const notDoneResearch = user.value.researches.filter((el) => !el.done)
  notDoneResearch.forEach((el, index) => {
    setTimeout(() => {
      el.done = true
      el.effect = true
      isShowSnackbar.value = true
      setDoneResearch(id, el.id)
    }, (index + 1) * 5000)
  })
})

const exitAction = () => {
  localStorage.clear()
  Router.push("/")
}

const goResearch = (research) => {
  const {id} = research
  Router.push(`/research/${id}`)
}


const formatDate = (date) => new Date(date).toLocaleDateString()


const formatTime = (date) => new Date(date).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"})


</script>

<template>
  <div class="account-page bg-indigo-lighten-5">
    <v-app-bar :elevation="2" color="indigo">
      <template v-slot:prepend>
        <v-icon icon="mdi-school-outline"/>
      </template>

      <v-app-bar-title>Распознователь потенциалов</v-app-bar-title>

      <template v-slot:append>
        <v-btn icon="mdi-account" @click="() => Router.push('/account')"></v-btn>
        <v-btn icon="mdi-exit-to-app" @click="exitAction"></v-btn>
      </template>
    </v-app-bar>

    <v-container v-if="isLoading" class="loading-container d-flex align-center justify-center">
      <v-progress-circular indeterminate :size="40" :width="5" color="indigo"></v-progress-circular>
    </v-container>


    <v-container v-else class="content">
      <v-card color="indigo" class="pa-4 f-flex align-center justify-center rounded-xl">
        <h2 class="mb-3">Информация об аккаунте</h2>

        <v-card class="d-flex align-center pa-3 rounded-xl">
          <v-icon class="mr-4" icon="mdi-account-circle" size="100" color="indigo-darken-1"/>
          <div>
            <v-chip class="account-count mb-1" color="indigo" density="comfortable">
              Исследований: {{ user.count }}
            </v-chip>
            <h3 class="account-name">{{ user.surname }} {{ user.name }}</h3>
            <div class="account-position">{{ user.position }}</div>

          </div>

        </v-card>
      </v-card>

      <div class="d-flex align-center justify-space-between">
        <h2 class="my-3">Результаты исследования</h2>
        <v-btn
          @click="() => {Router.push('create')}"
          variant="tonal"
          color="indigo-darken-1"
          append-icon="mdi-plus"
          type="submit"
        >Добавить
        </v-btn>
      </div>

      <div class="d-flex ga-3 flex-wrap">
        <v-row>
          <v-col v-for="research in user.researches" :key="research.fileName" sm="6" lg="4" cols="12">
            <v-card class="research d-flex flex-column align-center justify-center pa-3 text-center rounded-xl"
                    :class="{zoomElement: research.effect}">
              <v-icon icon="mdi-file-document" color="indigo-darken-1" size="50"/>
              <pre class="mb-4">{{ research.fileName }}</pre>
              <h3 class="research-name">{{ research.name }}</h3>
              <!--              <div class="account-position text-body-2">Пациент: {{ research.person }}</div>-->
              <div class="account-position text-body-2">{{ formatTime(research.date) }} |
                {{ formatDate(research.date) }}
              </div>
              <div class="account-position text-body-2 font-weight-medium my-2">Статус:
                {{ research.done ? "Готово" : "В обработке" }}
              </div>

              <v-btn
                @click="() => {goResearch(research)}"
                color="indigo"
                append-icon="mdi-chevron-right"
                type="submit"
                :disabled="!research.done"

              >Подробнее
              </v-btn>

            </v-card>
          </v-col>
        </v-row>


      </div>


    </v-container>

    <v-snackbar
      v-model="isShowSnackbar"
      timeout="3000"
      color="green-darken-3">
      Ваше исследование готово!

      <template v-slot:actions>
        <v-btn
          @click="() => isShowSnackbar = !isShowSnackbar"
          color="white"
          variant="text"
          icon="mdi-close"
        >
        </v-btn>
      </template>
    </v-snackbar>

  </div>
</template>

<style scoped>
.account-page {
  min-height: calc(100vh - 64px);
}

.loading-container {
  height: calc(70vh - 120px);
}

.research {
  border: 3px solid white;
}

.zoomElement {
  animation-name: zoomEffect;
  animation-duration: 0.6s;
  animation-iteration-count: 1;
  animation-timing-function: ease-in;
}

@keyframes zoomEffect {
  0% {
    border: 3px solid white;
  }
  50% {
    border: 3px solid #4758b8;
  }
  100% {
    border: 3px solid white;
  }
}
</style>
