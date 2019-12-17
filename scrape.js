const fs = require('fs');
const fetch = require('node-fetch');
const util = require('util');
const fs_writeFile = util.promisify(fs.writeFile);

let raw = fs.readFileSync('all_ids.json');
let ids = JSON.parse(raw);

async function doit() {
    const ts = [];
    for (let id of ids) {

        const url = `https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?Search=1&SchoolID=${id}&SchoolType=1&SchoolType=2&SchoolType=3&SchoolType=4&SpecificSchlTypes=all&IncGrade=-1&LoGrade=-1&HiGrade=-1&ID=${id}`
        const t = fetch(url)
        .then(resp => {
            if (resp.ok) {
                return resp.text();
            }
            else {
                throw new Error('resp.ok = false')
            }
        })
        .then(html => {
            return fs_writeFile(`out/${id}.html`, html);
        });
        .catch(err => {
            console.log(`${id} failed with error ${err}`);
        })
        ts.push(t);
    }

    console.log('All queued');
    for (let t of ts) {
        await t;
    }

    console.log('All done');
}

doit();
