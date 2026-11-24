import './style.css'
import heroImg from './assets/hero.png'
import typescriptLogo from './assets/typescript.svg'
import viteLogo from './assets/vite.svg'
import get_data from './read_excel';

let skill_arr=get_data("Skills.xlsx");
console.log(skill_arr);