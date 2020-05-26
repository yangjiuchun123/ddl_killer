import { JSEncrypt } from 'jsencrypt'
import getPubKey from '@/api/user'

const pub_key = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCt1/hVqW9pxTAp6vbJu5+5myvA\nF8wvsEqM7FdIAKe5hhD1paQhPcG/RkPFzQG1u0jeQcwNJIddhmk/jqAK0v2GbHhV\nUEw/rQ8AATFxLTitXWhjFPC2quAlGRzRby4LALxlWBziGNzKU6BERsI1nawJb1If\ni/+q/qgZMCAGKY1EAwIDAQAB\n-----END PUBLIC KEY-----'

// export function encrypt(password) {
//     let encrypt = new JSEncrypt()

//     getPubKey().then(res => {
//         // res : {'pub_key': pub_key, 'key_id': key.id}
//         encrypt.setPublicKey(res.pub_key)
//         return encrypt.encrypt(res.key_id + "|" + password)
//     })
    
// }

export function encrypt(password) {
    let enc = new JSEncrypt()
    enc.setPublicKey(pub_key)
    return enc.encrypt(password)
}