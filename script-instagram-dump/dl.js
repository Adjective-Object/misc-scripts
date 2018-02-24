const puppeteer = require("puppeteer");

function shuffle(array) {
  var currentIndex = array.length,
    temporaryValue,
    randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

const pageUrl = "https://www.instagram.com/adjectiveobject/";

async function listPosts(page) {
  let numPosts = await page.evaluate(() =>
    parseInt(document.querySelector("._fd86t").innerText)
  );
  let foundPosts = new Set();
  while (foundPosts.size < numPosts) {
    let urls = await page.evaluate(() => {
      let links = Array.from(document.querySelectorAll('a[href^="/p/"]')).map(
        a => a.href
      );
      window.scrollTo(
        0,
        document.querySelector("._havey").getBoundingClientRect().height
      );
      return links;
    });
    console.log(" urls: ", urls.length);
    urls.map(e => foundPosts.add(e));
    console.log("posts: ", foundPosts.size, "/", numPosts);
    await sleep(2000);
  }
  return shuffle(Array.from(foundPosts));
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto(pageUrl);
  let posts = await listPosts(page);
  console.log(posts);

  let i = 0;
  for (let post of posts) {
    i++;
    console.log(`[${i}/${posts.length}] nav to ${post}`);
    await page.goto(post);
    let resolutions = await page.evaluate(() => {
      let video = document.querySelector("video");
      let image = document.querySelector("._4rbun img");
      if (video) {
        return { "1": video.src };
      }

      return image.srcset
        .split(",")
        .map(s => s.split(" ").reverse())
        .reduce((a, b) => {
          let key = Array.from(b[0])
            .filter(n => !isNaN(parseFloat(n)) && isFinite(n))
            .join("");
          return Object.assign(a, { [key]: b[1] });
        }, {});
    });

    let numbers = Object.keys(resolutions)
      .slice()
      .map(x => parseInt(x));
    let biggestResolution = Math.max.apply(Math, numbers);
    console.log("resolution:", biggestResolution);
    console.log("url:", resolutions[biggestResolution]);

    await sleep(1000);
  }

  await browser.close();
})();
