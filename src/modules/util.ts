export function btnGroupClick(btnDiv: string, event: any): string {
  document.querySelectorAll(`#${btnDiv} .btn`).forEach((elem) => {
    elem.className = elem.className.replace(" active", "");
  });
  event.target.className += " active";
  return event.target.value;
}
