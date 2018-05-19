const READ = 1001;
const WRITE = 1002;

export default function hasPermission (el, bindings, vnode) {
    const security = vnode.context.$security;
    const {predicat, target} = parsePredicat(bindings.rawName);

    security.table['access-user'].forEach(accesRule => {
    });

    el.style.display = 'none';
}

function parsePredicat(rawValue) {
    const rawChunks = rawValue.split('.');
    const [_directive, target, predicat] = rawChunks;

    return {
        predicat: predicat,
        target: target
    }
}
