<script setup>
import {ref} from "vue";
import {useAPI, USER_ID} from "@/hooks/useAPI";
import {useRouter} from "vue-router";

const Router = useRouter()

const isShowPassword = ref(false)
const mail = ref("")
const password = ref("")
const isShowSnackbar = ref(false)

const {login, isLoading} = useAPI()

const submitHandler = async (event) => {
  event.preventDefault()
  isShowSnackbar.value = false
  const user = await login({mail: mail.value, password: password.value})
  if (user) {
    localStorage.setItem(USER_ID, user.id)
    await Router.push({path: "/account"})
  } else {
    isShowSnackbar.value = true
  }

}


</script>


<template>
  <div class="bg-indigo-lighten-5 w-100 h-100 d-flex align-center justify-center">
    <form class="d-flex flex-column align-center ga-5" @submit="submitHandler">
      <v-card class="py-3 px-5 rounded-xl" color="indigo">
        <h2>Распознователь потенциалов</h2>
      </v-card>

      <v-card class="login-card pa-4 rounded-xl">
        <h2 class="text-center my-3">Вход в систему</h2>

        <v-text-field
          v-model="mail"
          color="indigo"
          type="email"
          label="Электронная почта"
          variant="outlined"
          prepend-inner-icon="mdi-email"
          required
        />
        <v-text-field
          v-model="password"
          color="indigo"
          @click:append-inner="() => isShowPassword = !isShowPassword"
          :type="isShowPassword ? 'text' : 'password'"
          :append-inner-icon="isShowPassword ? 'mdi-eye' : 'mdi-eye-off'"
          label="Пароль" variant="outlined"
          prepend-inner-icon="mdi-key"
          required
        />
        <div class="d-flex align-center justify-center flex-column">
          <a
            class="text-decoration-none text-indigo mt-1 mb-4"
            rel="noopener noreferrer"
            target="_blank"
            href="#"
          >
            Вас нет в системе? Зарегистрироваться
            <v-icon icon="mdi-chevron-right"></v-icon>
          </a>

          <v-btn
            size="large"
            color="indigo"
            append-icon="mdi-chevron-right"
            type="submit"
            :loading="isLoading"
          >Войти
          </v-btn>


        </div>

      </v-card>

    </form>

    <v-snackbar
      v-model="isShowSnackbar"
      timeout="1500">
      Такой пользователь не найден. Попробуйте снова

      <template v-slot:actions>
        <v-btn
          color="red"
          variant="text"
          icon="mdi-close"
          @click="() => isShowSnackbar = !isShowSnackbar"
        >
        </v-btn>
      </template>
    </v-snackbar>

  </div>
</template>


<style>
.login-card {
  max-width: 500px;
  width: calc(100vw - 20px)
}

.login-card .v-field__append-inner {
  cursor: pointer !important;
}
</style>
