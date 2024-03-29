<template>
  <div class="fullscreen">
    <div v-if="loading" class="d-flex justify-content-center align-middle my-5">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div class="container">
      <div v-if="error && !allow_load_qr" class="alert alert-danger" role="alert">
        <i class="fa-solid fa-circle-exclamation text-danger"></i> {{ error }}
      </div>

      <div v-if="show_choose_concert" class="card">
        <h5 class="card-header">Выберите концерт</h5>
        <div class="card-body">
          <div class="d-grid gap-2">
            <button v-for="concert in concerts" class="btn btn-secondary" @click="chooseConcert(concert)">
              {{ concert.title }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <qrcode-stream v-if="allow_load_qr" :camera="camera" :torch="torch" @decode="onDecode" @init="onInit">

      <div v-if="!loading" class="container my-3 text-center">
        <div class="card">
          <div class="card-body">

            <div v-if="error" class="alert alert-danger" role="alert">
              <i class="fa-solid fa-circle-exclamation text-danger"></i> {{ error }}
            </div>

            <div v-for="ticket in decoded_tickets">

              <div v-if="ticket.state === 'done' && ticket.valid" class="alert alert-success" role="alert">
                <i class="fa-solid fa-circle-check text-success"> </i>
                Билет номер {{ ticket.number }}, {{ ticket.transaction.user.first_name }}. Валидирован.
                <a :href="ticket.url" class="link-secondary" target="_blank">Открыть билет.</a>
              </div>

              <div v-else class="alert alert-danger" role="alert">
                <div v-if="ticket.state === 'error'">{{ ticket.error }}</div>
                <div v-else>
                  <i class="fa-solid fa-circle-exclamation text-danger"> </i>
                  Билет номер {{ ticket.number }}, {{ ticket.transaction.user.first_name }}.
                  <span v-if="!ticket.is_active">Билет уже использован. </span>
                  <span v-if="!ticket.transaction.is_done">Билет не оплачен. </span>
                  <span v-if="ticket.concert_id !== current_concert_id">Билет оформлен не на этот концерт. </span>
                  <a :href="ticket.url" class="link-secondary" target="_blank">Открыть билет.</a>
                </div>
              </div>

            </div>

            <span v-if="decoded_tickets.length === 0">Ожидание QR-кода...</span>
            <p class="card-text"><small class="text-muted">Горный Чай © {{ current_year }}</small></p>

          </div>
        </div>

        <div class="fixed-bottom container mb-3">
          <div class="card">
            <div class="card-body">
              <p class="card-text"><small class="text-muted">{{ concert_title }}</small></p>
              <div class="d-grid gap-2">
                <a class="btn btn-secondary" href="/staff/"><i class="fa-solid fa-house"></i></a>
                <button class="btn btn-secondary" @click="changeCamera">
                  <i class="fa-solid fa-camera-rotate"></i>
                </button>
                <button v-if="torch_is_supported" class="btn btn-secondary" @click="torch = !torch">
                  <i class="fa-solid fa-bolt-lightning"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

    </qrcode-stream>
  </div>
</template>

<script>
import {QrcodeStream} from 'vue3-qrcode-reader'

export default {
  data() {
    return {
      camera: 'auto',
      torch: false,

      torch_is_supported: false,

      decoded_tickets: [],
      concerts: [],
      current_concert_id: null,
      concert_title: null,

      loading: true,
      allow_load_qr: false,
      show_choose_concert: false,
      error: '',
    }
  },
  components: {
    QrcodeStream
  },
  methods: {
    chooseConcert(concert) {
      this.current_concert_id = concert.id
      this.concert_title = concert.title
      this.loading = true
      this.show_choose_concert = false
      this.allow_load_qr = true
    },
    isValidHttpUrl(string) {
      let url;
      try {
        url = new URL(string);
      } catch (_) {
        return false;
      }
      return url.protocol === "http:" || url.protocol === "https:";
    },
    getTicketData(url) {
      let components = url.split('/')
      let req_url = `${base_url}/private/api/v1/tickets/${components[5]}/check/${components[6]}/${this.current_concert_id}/`;
      this.axios.put(req_url, {withCredentials: true})
          .then((response) => {
            response.data.state = 'done'
            this.push_to_query(response.data)
          })
          .catch((error) => {
            if (response.data) {
              response.data.state = 'error'
              this.push_to_query(response.data)
            } else {
              this.error = 'Неверный QR-код.'
              console.log(error);
            }
          })
    },
    push_to_query(element) {
      if (this.decoded_tickets.length === 3) {
        this.decoded_tickets[2] = this.decoded_tickets[1]
        this.decoded_tickets[1] = this.decoded_tickets[0]
        this.decoded_tickets[0] = element
      } else {
        this.decoded_tickets.push(element)
      }
    },
    onDecode(decodedString) {
      this.error = ''
      if (this.isValidHttpUrl(decodedString)) {
        this.getTicketData(decodedString)
      } else {
        this.error = 'Неверный QR-код.'
      }
    },
    changeCamera() {
      if (this.camera === 'rear' || this.camera === 'auto') {
        this.camera = 'front'
      } else {
        this.camera = 'rear'
      }
    },
    fetchConcerts() {
      let url = `${base_url}/private/api/v1/concerts/`
      this.axios.get(url, {withCredentials: true, params: {is_active: true}})
          .then((response) => {
            if (response.data.length === 0) {
              this.error = 'Нет доступных концертов.'
              this.loading = false
            } else {
              this.concerts = response.data
              this.loading = false
              this.show_choose_concert = true
            }
          })
          .catch((error) => {
            this.error = "Упс! Произошла ошибка, пожалуйста, сообщите нам."
            this.loading = false
            console.log(error);
          })
    },
    async onInit(promise) {
      this.error = ""
      try {
        const {capabilities} = await promise
        this.torch_is_supported = !!capabilities.torch
      } catch (error) {
        if (error.name === 'NotAllowedError') {
          this.error = "Чтобы продолжить, перезагрузите страницу и разрешите доступ к камере."
        } else if (error.name === 'NotFoundError') {
          this.error = "У вас нет камеры."
        } else if (error.name === 'NotSupportedError') {
          this.error = "Страница не загружена через HTTPS или localhost."
        } else if (error.name === 'NotReadableError') {
          this.error = "Возможно ваша камера используется другим приложением, проверьте и перезагрузите страницу."
        } else if (error.name === 'OverconstrainedError') {
          this.error = "Вы пытались включить фронтальную камеру несмотря на то, что ее нет?"
        } else if (error.name === 'StreamApiNotSupportedError') {
          this.error = "Ваш браузер не поддерживается."
        }
      } finally {
        this.loading = false;
      }
    }
  },
  computed: {
    base_url: function () {
      return window.base_url
    },
    current_year: function () {
      let date = new Date()
      return date.getFullYear()
    }
  },
  mounted() {
    this.fetchConcerts()
  }
}
</script>

<style>
.fullscreen {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background-color: black;
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
}
</style>
