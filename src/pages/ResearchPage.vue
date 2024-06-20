<script setup>
import {useRoute, useRouter} from "vue-router";
import {onMounted, ref} from "vue";
import {useAPI, USER_ID} from "@/hooks/useAPI";

const {getResearch, dataTableGenerator} = useAPI()
const Router = useRouter()
const {params} = useRoute()
const research = ref(null)
const isOpen = ref(false)
const imageLink = ref("")


const dataTable = ref([])


const researchID = params.id;
if (!researchID)
  Router.push("/account")
const userID = Number(localStorage.getItem(USER_ID))
if (!userID)
  Router.push("/")

onMounted(async () => {
    research.value = await getResearch(userID, researchID)
    dataTable.value = dataTableGenerator()
    isLoading.value = false

  }
)

const isLoading = ref(true)

const exitAction = () => {
  localStorage.clear()
  Router.push("/")
}

const openImageHandler = (tr) => {
  imageLink.value = `/src/assets/research/${researchID}/${research.value.image[tr.index % research.value.image.length]}`
  isOpen.value = !isOpen.value

}

const value = ref([
  423,
  446,
  675,
  510,
  590,
  610,
  760,
])

const formatDate = (date) => new Date(date).toLocaleDateString()

const formatTime = (date) => new Date(date).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"})
</script>

<template>
  <div class="research-page bg-indigo-lighten-5">
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
      <h2 class="mb-3">Информация о исследовании "{{ research.name }}"</h2>
      <v-card class="pa-3">
        <v-row align="center">
          <v-col cols="12" sm="6" md="4" class="d-flex flex-column justify-center align-center">
            <v-icon class="my-5" icon="mdi-file-document" color="indigo-darken-1" size="60"/>
            <div class="id-research"><b>Имя файла:</b> {{ research.fileName }}</div>
            <div class="date-research"><b>Дата:</b> {{ formatTime(research.date) }} |
              {{ formatDate(research.date) }}
            </div>
            <div class="status-research"><b>Статус:</b> Готово</div>
            <v-btn
              class="my-2"
              color="indigo"
              append-icon="mdi-download"
            >Скачать
            </v-btn>
          </v-col>
          <v-col cols="12" sm="6" md="8" class="d-flex flex-column justify-center">
            <v-text-field
              class="mt-2"
              v-model="research.offset"
              label="Смещение времени"
              variant="outlined"
              readonly
              autofocus
            />
            <v-text-field
              v-model="research.layout"
              label="Расскладка датчиков"
              variant="outlined"
              readonly
            />
            <p class="text-caption mb-7">Интервал для построения графиков:</p>
            <v-range-slider
              v-model="research.interval"
              strict
              min="-1000"
              max="1000"
              step="10"
              color="indigo"
              thumb-label="always"
              readonly
              @blur="(event) => {event.target.focus()}"

            ></v-range-slider>
          </v-col>
        </v-row>


        <h3 class="mb-2">Результат исследования</h3>
        <v-row class="mt-1">
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="research.label50"
              class="mt-2 selected"
              label="P50"
              color="green"
              focused
              variant="outlined"
              readonly
              @blur="(event) => {event.target.focus()}"
            />
            <v-text-field
              v-model="research.label175"
              class="mt-2 selected"
              color="green"
              label="P175"
              variant="outlined"
              readonly
              focused
              @blur="(event) => {event.target.focus()}"
            />
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="research.label100"
              class="mt-2 selected"
              color="green"
              label="P100"
              variant="outlined"
              focused
              readonly
              @blur="(event) => {event.target.focus()}"
            />

            <v-text-field

              v-model="research.label300"
              class="mt-2 selected"
              label="P300"
              color="green"
              variant="outlined"
              focused
              readonly
            />

          </v-col>
        </v-row>
        <v-text-field
          v-model="research.speed"
          class="mt-2 selected"
          label="Скорость реакции на объекты"
          variant="outlined"
          color="green"
          focused
          readonly
        />

        <!--        =======================-->
        <div class="d-none d-md-block">
          <h3 class="mb-3">Табличные данные</h3>
          <v-table hover>
            <thead>
            <th>
              №
            </th>
            <th>
              Диапазон
            </th>
            <th>
              Потенциалы
            </th>
            <th>
              Отклонения от нормы
            </th>
            <th>
              Время возникновения (ms)
            </th>
            <th>
              Действия
            </th>
            </thead>
            <tbody>
            <tr v-for="tr in dataTable" :key="tr.index">
              <td class="text-center">{{ tr.index }}</td>
              <td class="text-center">
                <v-chip variant="outlined">{{ tr.range }}</v-chip>
              </td>
              <td class="text-center">
                <v-chip v-for="potential in tr.potentials.split('|')" :key="potential" color="indigo" class="pm-1"
                        variant="outlined" density="compact">
                  {{ potential }}
                </v-chip>
              </td>
              <td class="text-center">
                <v-chip color="green-darken-1" variant="outlined">{{ tr.deviations }}</v-chip>
              </td>
              <td class="text-center">
                <v-chip v-for="duration in tr.duration.split('|')" :key="duration" color="green-darken-1" class="pm-1"
                        variant="outlined" density="compact">
                  {{ duration }}
                </v-chip>
              </td>
              <td class="text-center">
                <v-btn
                  @click="() => {openImageHandler(tr)}"
                  class="my-2"
                  variant="outlined"
                  color="indigo"
                  icon="mdi-select-search"
                  density="comfortable"
                >
                </v-btn>
              </td>
            </tr>
            </tbody>
          </v-table>
        </div>

        <div class="d-block d-md-none">
          <v-expansion-panels variant="accordion" elevation="0">
            <v-expansion-panel
              v-for="tr in dataTable"
              :key="tr.index"
            >
              <v-expansion-panel-title>
                <div class="d-flex align-center justify-center">
                  <v-chip class="mr-3" variant="elevated" color="green">Номер: {{ tr.index }}</v-chip>
                  <div class="font-weight-bold">{{ tr.range }}</div>
                </div>

              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div class="expansion-content-wrapper">
                  <div class="d-flex align-center justify-start ga-1 mb-3">
                    <span>Потенциалы: </span>
                    <v-chip v-for="potential in tr.potentials.split('|')" :key="potential" color="indigo" class="pm-1"
                            variant="outlined" density="compact">
                      {{ potential }}
                    </v-chip>
                  </div>

                  <div class="d-flex align-center justify-start ga-1 mb-3">
                    <span>Время: </span>
                    <v-chip v-for="duration in tr.duration.split('|')" :key="duration" color="green-darken-1"
                            class="pm-1"
                            variant="outlined" density="compact">
                      {{ duration }}
                    </v-chip>
                  </div>

                  <div class="d-flex align-center justify-start ga-1 mb-2">
                    <span>Отклонение от нормы: </span>
                    <v-chip color="green-darken-1" variant="outlined" density="compact">{{ tr.deviations }}</v-chip>
                  </div>


                  <v-timeline direction="horizontal" dot-color="green" line-color="green-lighten-3"
                              density="compact" size="15">
                    <v-timeline-item>
                      <div class="text-center text-caption">0</div>
                    </v-timeline-item>


                    <v-timeline-item v-for="(potential, index) in tr.potentials.split('|')" :key="potential">

                      <div class="text-center text-caption">{{ tr.duration.split('|')[index] }} | {{ potential }}</div>
                    </v-timeline-item>


                    <v-timeline-item>
                      <div class="text-center text-caption">400</div>
                    </v-timeline-item>
                  </v-timeline>


                  <div class="d-flex align-center justify-end">
                    <v-btn
                      @click="() => {openImageHandler(tr)}"
                      class="my-2"
                      variant="flat"
                      color="indigo"
                      prepend-icon="mdi-select-search"

                    > График
                    </v-btn>
                  </div>

                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>

      </v-card>

    </v-container>

    <v-dialog
      v-model="isOpen"
      width="auto"
      transition="dialog-bottom-transition"
    >
      <v-card
        prepend-icon="mdi-update"
        title="График"
      >
        <v-card-item>
          <v-img :src="imageLink" width="800px"/>
        </v-card-item>
        <template v-slot:actions>
          <v-btn
            class="ms-auto"
            text="Закрыть"
            @click="() => {isOpen = !isOpen}"
          ></v-btn>
        </template>
      </v-card>
    </v-dialog>

  </div>
</template>

<style scoped>
.research-page {
  min-height: calc(100vh - 64px);
}

.loading-container {
  height: calc(70vh - 120px);
}

.pm-1 {
  margin-left: 2px;
  margin-right: 2px;
}

</style>
