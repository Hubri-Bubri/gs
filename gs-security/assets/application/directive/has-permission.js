import _ from 'lodash';


const PredicateCode = {
    'read': 1001,
    'write': 1002,
    'update': 1003,
    'delete': 1004
};


function parsePermission(rawValue) {
    const rawChunks = rawValue.split('.');
    const [_directive, target, predicate] = rawChunks;

    return {
        predicate: predicate,
        target: target
    }
}

export function hasPermission(accesRules, target, predicate) {

    return _.chain(accesRules).map(accesRule => {
            return _.startsWith(accesRule.target, target) && _.includes(accesRule.permission, PredicateCode[predicate]);
        })
        .includes(true)
        .value();
}

export function hasPermissionDirective(el, bindings, vnode) {
    const security = vnode.context.$security;
    const { target, predicate } = parsePermission(bindings.rawName);
    const isHasPermission = hasPermission(security.table['access-user'], target, predicate);

    if (!isHasPermission) {
        el.style.display = 'none';
    }
}
