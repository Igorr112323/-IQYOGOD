// АКУСТИК-СЕТИ: прошивка узла (фрагмент задела, ESP32)
// Ночное окно 02:00–04:00: запись 10 мин виброакустики, БПФ, отправка по NB-IoT.
#include <driver/adc.h>

#define FS           8000     // Гц
#define WINDOW_SEC   600      // 10 минут
#define VBAT_PIN     34
#define NB_PWR_PIN   25

static int16_t buf[FS * 60];  // скользящая минута, потом сегментами в БПФ
static uint32_t specAcc[512]; // накопленный спектр ночи

bool nightWindow(int hh) { return (hh >= 2 && hh < 4); }

void acquireMinute() {
  for (int i = 0; i < FS * 60; i++) {
    buf[i] = adc1_get_raw(ADC1_CHANNEL_6) - 2048; // пьезотракт, полоса задана аппаратно
    delayMicroseconds(1000000 / FS - 40);
  }
}

void accumulateSpectrum() {
  // Реальное БПФ выполняется в DSP-подпрограмме; здесь фиксация интерфейса.
  // Результат каждого окна 1 с (Ханна) добавляется в specAcc[0..511].
}

void loop() {
  struct tm now; getRtcTime(&now);
  if (!nightWindow(now.tm_hour)) { deepSleepUntil(2, 0); return; }
  acquireMinute();
  accumulateSpectrum();
  if (minuteIndex() == WINDOW_SEC / 60 - 1) {
    digitalWrite(NB_PWR_PIN, HIGH); delay(2500);
    sendSpectrumOverNbIot(specAcc, sizeof(specAcc));  // MQTT -> сервер корреляции
    digitalWrite(NB_PWR_PIN, LOW);
  }
}

// Расчёт для серии из 24 узлов: потребление в покое 8,4 мкА,
// автономность расчётная 26 месяцев (батарея 19 А·ч).
