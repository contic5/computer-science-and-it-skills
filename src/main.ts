import './style.css'
import heroImg from './assets/hero.png'
import typescriptLogo from './assets/typescript.svg'
import viteLogo from './assets/vite.svg'
import get_data from './read_excel';

async function setup()
{
  skill_arr=await get_data("src/results/Analyzed Skills Stable.xlsx");
  console.log(skill_arr);
}

let skill_arr:any[]=[]; 
setup();