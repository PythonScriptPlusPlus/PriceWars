/* eslint-disable import/prefer-default-export */
/* eslint-disable consistent-return */
/* eslint-disable arrow-body-style */
/* eslint-disable import/no-extraneous-dependencies */
import Swal from 'sweetalert2';

const screens = [
  {
    title: '<h3 class="alert__header">Добро пожаловать в игру!</h3>',
    html: '<p class="alert__text">В этой игре вы выполняете роль фирмы-монополиста. Ваша цель - управлять производством и некоторыми другими аспектами бизнеса, чтобы не допустить вход конкурентов на рынок и их укрепления там.</p>',
    confirmButtonText: 'Хорошо',
    confirmButtonColor: '#3085d6',
    draggable: true,
    showCloseButton: true,
  },
  {
    title: '<h3 class="alert__header">Нужно обучение?</h3>',
    html: '<p class="alert__text">выбор потом можно будет поменять в настройках</p>',
    showCloseButton: true,
    showDenyButton: true,
    confirmButtonText: 'Да',
    denyButtonText: 'Нет',
    icon: 'question',
    confirmButtonColor: '#0db400',
    cancelButtonColor: '#c30000',
  },
  {
    title: '<h3 class="alert__header">Обучение</h3>',
    html: '<p class="alert__text">Механика игры построена на простой функции спроса и стоимости производства. Обе эти величены вы можете найти в правом верхнем углу экрана. Его можно пролистать по-горизонтали, если не всё видно.</p>',
    confirmButtonText: 'Далее',
    confirmButtonColor: '#3085d6',
    showCloseButton: true,
  },
  {
    title: '<h3 class="alert__header">Как производить оптимально?</h3>',
    html: '<p class="alert__text">Эта игра считает прибыль по формуле:</p><div id="latex-formula">$$\\pi(q) = (100 - Q)q - cq$$</div><p class="alert__text">где содержимое скобок - функция спроса; Q - количество произведённой продукции вами и вашим оппонентом; c - стоимость производства одной единицы товара, а q - то, сколько товара произвели вы. Произведя вычисления с помощью производных вы можете найти оптимальное количество продукта</p>',
    confirmButtonText: 'Понятно',
    showCancelButton: true,
    cancelButtonText: 'Назад',
    showCloseButton: true,
    confirmButtonColor: '#3085d6',
    footer: '<p class="alert__text">Если вы не знате, как это рассчитывается, то можете обратиться к этой <a href="https://ecson.ru/economics/market-structure-analysis/zadacha-152.raschyot-optimalnogo-objoma-vypuska.tseny-i-pribyli-monopolista.html" target="_blank" rel="noopener noreferrer">статье</a></p>',
    didOpen: () => {
      if (window.MathJax) {
        window.MathJax.typesetPromise();
      }
    },
  },
  {
    title: '<h3 class="alert__header">Попробуйте сами!</h3>',
    html: '<p class="alert__text">Теперь вы можете применить полученные знания на практике. Удачи в игре!</p>',
    confirmButtonText: 'Начать',
    confirmButtonColor: '#3085d6',
    showCloseButton: true,
    stop: true,
  },
  {
    title: '<h3 class="alert__header">Хорошая работа!</h3>',
    html: '<p class="alert__text">Вы получили первую прибыль! Теперь попробуйте накопить денег до 9 периода.</p>',
    confirmButtonText: 'Ок',
    confirmButtonColor: '#3085d6',
    showCloseButton: true,
    stop: true,
  },
  {
    title: '<h3 class="alert__header">Обратите внимание!</h3>',
    html: '<p class="alert__text">На рынок в следующем периоде войдёт оппонент. Теперь вам нужно учитывать его действия при планировании производства и стратегии ценообразования. Следите за изменениями на рынке и адаптируйте свою стратегию! Также посмотрите в другие вкладки справа. Они помогут вам против конкурентов</p>',
    confirmButtonText: 'Понятно',
    confirmButtonColor: '#f39c12',
    icon: 'warning',
    showCloseButton: true,
    stop: true,
  },
  {
    title: '<h3 class="alert__header">Лоббирование</h3>',
    html: '<p class="alert__text">В игре доступна опция лоббирования. Вы можете использовать её, чтобы повысить стоимость вхождения для конкурентов. Если у оппонента не найдётся денег чтобы "оплатить порог", то он не войдёт на рынок в тот период</p>',
    confirmButtonText: 'Понятно',
    confirmButtonColor: '#3085d6',
    showCloseButton: true,
    stop: true,
  },
  {
    title: '<h3 class="alert__header">Собственность</h3>',
    html: '<p class="alert__text">В игре доступна опция покупки собственности. Покупка собственности увеличивает ваши затраты в период в виде налогов, но в обмен увеличивает порог вхождения для оппонента.</p>',
    footer: '<a class="alert__text" id="why-property-link" style="cursor:pointer;">Почему так?</a>',
    confirmButtonText: 'Далее',
    confirmButtonColor: '#3085d6',
    showCloseButton: true,
    stop: true,
    didOpen: () => {
      const link = document.getElementById('why-property-link');
      if (link) {
        link.onclick = () => {
          Swal.fire({
            title: '<h3 class="alert__header">Это нестратегический барьер</h3>',
            html: '<p class="alert__text">Состояние инфраструктуры рынка в виде наличия и степени развитости транспортной системы и системы хранения товаров в регионе или стране в целом оказывает влияние на возможность перемещения товаров в рамках территорий и, следовательно, на наличие или отсутствие местных локальных рынков. Чем лучше развита инфраструктура рынка, тем быстрее товары могут перемещаться по территории, тем меньше вероятность возникновения замкнутого локального рынка, и тем более открытым будет продуктовый рынок в целом. Отсутствие нормально функционирующей транспортной системы и системы хранения товаров может препятствовать проникновению новых фирм на рынки и формированию достаточно замкнутых территориально ограниченных рыночных пространств.</p>',
            confirmButtonText: 'Понятно',
            confirmButtonColor: '#3085d6',
            showCloseButton: true,
          });
        };
      }
    },
  },
];

let screensIndex = 0;

export function showWelcomeAlert(setLearningMode, manualScreenIndex = -1, newGame = false) {
  if (newGame) {
    screensIndex = 0;
  }
  if (screensIndex >= screens.length) {
    return;
  }
  if (manualScreenIndex > screensIndex) {
    return Swal.fire({
      ...screens[manualScreenIndex],
    });
  }
  return Swal.fire({
    ...screens[screensIndex],
  }).then((result) => {
    const currentScreen = screens[screensIndex];

    if (result.isConfirmed && currentScreen && !currentScreen.stop) {
      screensIndex += 1;
      if (setLearningMode) setLearningMode(true); // checked
      showWelcomeAlert(setLearningMode);
    } else if (result.isDismissed && result.dismiss === Swal.DismissReason.cancel) {
      screensIndex -= 1;
      showWelcomeAlert(setLearningMode);
    } else if (result.isDenied || result.isDismissed === Swal.DismissReason.close) {
      if (setLearningMode) setLearningMode(false); // unchecked
      screensIndex = 0;
    }
    // Only check .stop if currentScreen exists
    if (currentScreen && currentScreen.stop) {
      screensIndex += 1;
    }
  });
}
