// functions.js

import { NAV_CLASSES } from '../dashboard_const.js';

export function toggleView(viewId) {
    document.getElementById('projects-view').style.display = 'none';
    document.getElementById('dashboard-view').style.display = 'none';

    document.getElementById(viewId).style.display = 'block';
}

export function setActiveNavItem(element) {
    document.querySelectorAll(`.${NAV_CLASSES.NAV_ITEM}`).forEach(item =>
        item.classList.remove(NAV_CLASSES.ACTIVE)
    );
    document.querySelectorAll(`.${NAV_CLASSES.SUB_NAV_ITEM}`).forEach(item =>
        item.classList.remove(NAV_CLASSES.ACTIVE)
    );
    element.classList.add(NAV_CLASSES.ACTIVE);
}

export function toggleSubNav(subNavId, chevronId) {
    const subNav = document.getElementById(subNavId);
    const chevron = document.getElementById(chevronId);
    subNav.classList.toggle('expanded');
    chevron.classList.toggle('expanded');
}