/**
 * 用 puppeteer 从 oddsportal 保存历史世界杯赔率
 * https://www.oddsportal.com/soccer/world/world-cup-2022/england-senegal-bswGq3oQ/#cs;2
 * 保存到 page 文件夹里
 */

const path = require("path");
const fs = require("fs");
var { parse } = require("csv-parse/sync");
const puppeteer = require("puppeteer");

const get = async (num, xeid, team1, team2) => {
  const browser = await puppeteer.launch({
    //  headless: false,
  });
  const page = await browser.newPage();

  await page.goto(
    `https://www.oddsportal.com/soccer/world/world-cup-2022/${team1}-${team2}-${xeid}/#cs;${num}`,
    {
      waitUntil: "domcontentloaded",
    }
  );

  await page.waitForSelector("#odds-data-table .avg.nowrp a");

  const html = await page.content();

  fs.writeFileSync(`cs${num}/` + xeid + ".html", html);

  await browser.close();
};

async function main() {
  // data = parse(fs.readFileSync("fifa2022.csv"));
  data = parse(fs.readFileSync("aa.csv"));
  
  
  for (let i = 20; i < data.length; i++) {
    console.log(i, data[i][0], data[i][8], data[i][9]);
    try {
        await get(4, data[i][0], data[i][8], data[i][9]);
    } catch(e) {
      try {
        await get(4, data[i][0], data[i][8], data[i][9]);
      } catch(e) {
      }
    }
  }
  for (let i = 1; i < data.length; i++) {
    console.log(i, data[i][0], data[i][8], data[i][9]);
    try {
        await get(3, data[i][0], data[i][8], data[i][9]);
    } catch(e) {
      try {
        await get(3, data[i][0], data[i][8], data[i][9]);
      } catch(e) {
      }
    }
  }
  for (let i = 12; i < data.length; i++) {
    console.log(i, data[i][0], data[i][8], data[i][9]);
    try {
        await get(2, data[i][0], data[i][8], data[i][9]);
    } catch(e) {
      try {
        await get(2, data[i][0], data[i][8], data[i][9]);
      } catch(e) {
      }
    }
  }
}

main();
