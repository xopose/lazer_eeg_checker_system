<script setup>
import Router from "@/router";
import {ref} from "vue";
import {useDisplay} from "vuetify";
import {useAPI, USER_ID} from "@/hooks/useAPI";

const {mobile: isMobile} = useDisplay()

const items = ref(["Шаг 1", "Шаг 2", "Шаг 3", "Шаг 4"])

const stage = ref(1)
const name = ref("")
const file = ref(null)
const offset = ref(0)
const interval = ref([-250, 750])
const layout = ref('1020')
const isShowSnackbar = ref(false)
const {isLoading, createResearch} = useAPI()

const id = Number(localStorage.getItem(USER_ID))

const exitAction = () => {
  localStorage.clear()
  Router.push("/")
}

const create = async () => {
  if (name.value && file.value) {
    const result = await createResearch(id, {
      fileName: file.value.name,
      name: name.value,
      person: "",
      date: new Date(),
      offset: offset.value,
      interval: interval.value,
      layout: layout.value,
      label50: "Отклонений не выявлено",
      label100: "Отклонений не выявлено",
      label175: "Отклонений не выявлено",
      label300: "Отклонений не выявлено",
      speed: "306 мс",
      image: ["1.png", "2.png", "3.png"],
      done: false
    })
    if (result)
      Router.push("/account")
  } else {
    isShowSnackbar.value = true
  }

}
</script>

<template>
  <div class="create-page bg-indigo-lighten-5">

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

    <v-container class="content">
      <h2 class="mb-3">Создание нового исследования</h2>

      <v-stepper
        v-model="stage"
        :items="items"
        next-text="Далее"
        prev-text="Назад"
        color="indigo"
        :mobile="isMobile"
      >
        <template v-slot:[`item.1`]>
          <v-sheet class="pa-1">
            <p class="text-subtitle-1 mb-3">Укажите название своего исследования:</p>
            <v-text-field
              v-model="name"
              label="Название"
              variant="outlined"
              required
            />


          </v-sheet>
        </template>

        <template v-slot:[`item.2`]>
          <v-sheet class="pa-1">
            <p class="text-subtitle-1 mb-3">Загрузите файл с результатими эксперимента:</p>
            <v-file-input
              v-model="file"
              label="Перетащите или выберите файл с данными"
              variant="outlined"
              show-size
              accept="text/plain"
            />


          </v-sheet>
        </template>

        <template v-slot:[`item.3`]>
          <v-sheet class="pa-1">
            <p class="text-subtitle-1 mb-3">Укажите смещение времени относительно начала эксперемента:</p>
            <v-text-field
              v-model="offset"
              label="Время начала эксперимента"
              variant="outlined"
              type="number"
              required
            />
            <p class="text-subtitle-1 mb-7">Укажите интервал для построения графиков:</p>
            <v-range-slider
              v-model="interval"
              strict
              min="-1000"
              max="1000"
              step="10"
              color="indigo"
              thumb-label="always"

            ></v-range-slider>


          </v-sheet>
        </template>

        <template v-slot:[`item.4`]>
          <v-sheet class="pa-1">
            <p class="text-subtitle-1 mb-3">Выбор расскладку датчиков в исследовании:</p>
            <v-radio-group
              class="fix-text"
              v-model="layout"
              color="indigo"
            >
              <v-radio
                label="1010"
                value="1010"
              ></v-radio>
              <v-radio
                label="1020"
                value="1020"
              ></v-radio>
            </v-radio-group>


          </v-sheet>
        </template>
      </v-stepper>

      <div class="d-flex justify-center align-center mt-5">
        <v-btn
          @click="create"
          :loading="isLoading"
          color="indigo"
          append-icon="mdi-plus"
          type="submit"
        >Создать
        </v-btn>
      </div>

    </v-container>
    <v-snackbar
      v-model="isShowSnackbar"
      timeout="1500">
      Необходимо заполнить все данные об исследовании

      <template v-slot:actions>
        <v-btn
          @click="() => isShowSnackbar = !isShowSnackbar"
          color="red"
          variant="text"
          icon="mdi-close"
        >
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<style scoped>
.create-page {
  min-height: calc(100vh - 64px);
}

</style>
