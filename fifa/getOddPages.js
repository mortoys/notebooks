/**
 * 用 puppeteer 从 oddsportal 保存历史世界杯赔率
 * 保存到 page 文件夹里
 */

const path = require("path");
const fs = require("fs");
const puppeteer = require('puppeteer');


const get = async (index) => {
    const browser = await puppeteer.launch({
        // headless: false,
    });
    const page = await browser.newPage();

    await page.goto(`https://www.oddsportal.com/soccer/world/world-championship-2022/results/#/page/${index}/`, {
        waitUntil: 'domcontentloaded'
    });

    await page.waitForSelector('.table-main .deactivate .result-ok a')

    const html = await page.content();
    
    fs.writeFileSync('page/' + index + '.html', html)


    await browser.close();
};

async function main() {
    for(let i = 0; i < 19; i++) {
        console.log('page: ' + (i+1));
        await get(i+1);
    }
}

main()