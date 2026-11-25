import './style.css'
import heroImg from './assets/hero.png'
import typescriptLogo from './assets/typescript.svg'
import viteLogo from './assets/vite.svg'
import get_data from './read_excel';

async function setup()
{
  skill_arr=await get_data("src/results/Analyzed Skills Stable.xlsx","Results");
  console.log(skill_arr);
  for(let skill of skill_arr)
  {
    //Create details accordion item
    let skill_details=document.createElement("details");
    if(skill.Category=="IT")
    {
      document.getElementById("it_skills")?.appendChild(skill_details);
    }
    else
    {
      document.getElementById("computer_science_skills")?.appendChild(skill_details);
    }
    skill_details.classList.add("accordion-item");

    //Create summary accordion header
    let skill_header=document.createElement("summary");
    skill_details.appendChild(skill_header);
    skill_header.classList.add("accordion-header");

    //Add short explanation to accordion head
    skill_header.innerHTML=`${skill.Skill}: ${skill.Short_Explanation}`;

    //Manually add open_svg to accordion header
    let open_svg='<svg class="accordion-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m2 5 6 6 6-6"/></svg>';
    skill_header.innerHTML+=open_svg;

    //Create skill body
    let skill_body=document.createElement("div");
    skill_details.appendChild(skill_body);
    skill_body.classList.add("accordion-body");
    
    //Add long explanation to accordion body
    let explanation_p=document.createElement("p");
    skill_body.appendChild(explanation_p);
    explanation_p.innerHTML=skill.Long_Explanation;

    //Create paragraph saying there are jobs
    let jobs_using_skill_p=document.createElement("p");
    skill_body.appendChild(jobs_using_skill_p);
    jobs_using_skill_p.innerHTML=`
    Jobs using ${skill.Skill}<br>`

    //Create an unordered list that contains each job that uses skill
    let jobs=skill.Jobs.split(",");
    let jobs_ul=document.createElement("ul");
    skill_body.appendChild(jobs_ul);
    for(let job of jobs)
    {
      let job_li=document.createElement("li");
      job_li.innerHTML=job;
      jobs_ul.appendChild(job_li);
    }

    
  }
}

let skill_arr:any[]=[]; 
setup();