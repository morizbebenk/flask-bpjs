## Flask BPJS

Webservice yang digunakan untuk menangani proses dekripsi respon data dari bridging BPJS VCLAIM REST 2.0 (Encrypted Version). Support VCLAIM v1 dan API JKN (Antrean RS).

## Kebutuhan

**Utama**

- Python

**Package**

- Flask
- lzstring
- requests
- flask_cors 
- pycryptodome 
- python-dotenv 

## Virtual Environment

Bagian ini opsional tetapi sangat disarankan untuk membuat virtual environment supaya ketika ada update package yang tidak support / bermasalah tidak akan mengganggu aplikasi lain.

### Membuat Virtual Environment

```bash
python -m venv virtualenv
```

atau

```bash
python3 -m venv virtualenv
```

### Aktivasi Virtual Environment

- **Windows**

    ```bash
    virtualenv\Scripts\activate
    ```

- **Bash**

    ```bash
    source virtualenv/bin/activate
    ```

### Instal Paket Python

```bash
pip install Flask lzstring requests flask_cors pycryptodome python-dotenv
```

## File .env
- Salin file `.env.example`
- Ubah nama file menjadi `.env`
- Lengkapi data `HOST`, `CONSID`, `SECRET`, `USER_KEY` & `IS_ENCRYPT`
- Host Development VClaim : https://apijkn-dev.bpjs-kesehatan.go.id/vclaim-rest-dev/
- Host Production VClaim : -
- Host Development API JKN : https://apijkn-dev.bpjs-kesehatan.go.id/antreanrs_dev/
- Host Production API JKN : -

## Pengaturan

### Setup Aplikasi

- **Windows**

    ```bash
    set FLASK_APP=app
    ```

- **Bash**

    ```bash
    export FLASK_APP=app
    ```

### Mode Debug

- **Windows**

    </> **Debug ON :**

    ```bash
    set FLASK_DEBUG=1
    ```

    </> **Debug OFF :**

    ```bash
    set FLASK_DEBUG=0
    ```

- **Bash**

    </> **Debug ON :**

    ```bash
    export FLASK_DEBUG=1
    ```

    </> **Debug OFF :**

    ```bash
    export FLASK_DEBUG=0
    ```

### Mode Environment

- **Windows**

    </> **Development :**

    ```bash
    set FLASK_ENV=development
    ```

    </> **Production :**

    ```bash
    set FLASK_ENV=production
    ```

- **Bash**

    </> **Development :**

    ```bash
    export FLASK_ENV=development
    ```

    </> **Production :**

    ```bash
    export FLASK_ENV=production
    ```

## Menjalankan Aplikasi

#### Cara Mudah

```bash
flask run
```

Secara default akan berjalan di `http://127.0.0.1:5000`.

#### Custom Host
```bash
flask run -h 0.0.0.0
```

Dapat diakses semua klien di jaringan yang sama.

#### Custom Port
```bash
flask run -p 8080
```

Berjalan di port 8080.

## Cara Pakai


#### Menggunakan Environment Credential

`host`, `consid`, `secret`, `user_key` dan `is_encrypt` mengambil data dari file `.env`.

| Request | Konten | Nilai | Keterangan |
| ------- | ------ | ----- | ---------- |
| Host | `http://127.0.0.1:5000` | - | Menyesuaikan host dan port yang di jalankan |
| Header | `Content-Type` | `application/json` | Wajib |
| Method | `POST` | - | Wajib POST |
| Body | `url` | `referensi/poli/ana` (contoh) | Wajib, mengacu dokumentasi VClaim BPJS tanpa base url. Contoh : `referensi/poli/ana` |
| Body | `method` | `GET` / `POST` / `PUT` / `DELETE` | Wajib, mengacu dokumentasi VClaim BPJS / API JKN |
| Body | `payload` | `{"request": {"t_sep": {"noSep": "0301R0011017V000007", "user": "Coba Ws"}}}` (contoh) | Opsional menyesuaikan rest VClaim BPJS / API JKN. Jika tidak ada data, payload diisi string kosong |

#### Menggunakan Header Credential

`host`, `consid`, `secret`, `user_key` dan `is_encrypt` mengambil data dari header yang dikirimkan, jika menggunakan metode ini diwajibkan mengirim data header `x-host`, `x-consid`, `x-secret`, `x-user_key` dan `x-is_encrypt` dengan lengkap, jika salah satu kosong atau tidak dikirim maka secara default akan menggunakan metode `Environment Credential` diatas.

| Request | Konten | Nilai | Keterangan |
| ------- | ------ | ----- | ---------- |
| Host | `http://127.0.0.1:5000` | - | Menyesuaikan host dan port yang di jalankan |
| Header | `Content-Type` | `application/json` | Wajib |
| Header | `x-host` | `https://apijkn-dev.bpjs-kesehatan.go.id/vclaim-rest-dev/` (host development) | Custom `host` |
| Header | `x-consid` | `1234` | Custom `consid` |
| Header | `x-secret` | `12345abcde` | Custom `secret` |
| Header | `x-user_key` | `1a2b3c4d5e6f7g8h9i10j` | Custom `user_key` untuk API JKN |
| Header | `x-is_encrypt` | `0` / `1` | Custom `is_encrypt` |
| Method | `POST` | - | Wajib POST |
| Body | `url` | `referensi/poli/ana` (contoh) | Wajib, mengacu dokumentasi VClaim BPJS tanpa base url. Contoh : `referensi/poli/ana` |
| Body | `method` | `GET` / `POST` / `PUT` / `DELETE` | Wajib, mengacu dokumentasi VClaim BPJS / API JKN |
| Body | `payload` | `{"request": {"t_sep": {"noSep": "0301R0011017V000007", "user": "Coba Ws"}}}` (contoh) | Opsional menyesuaikan rest VClaim BPJS / API JKN. Jika tidak ada data, payload diisi string kosong | 

## Sumber Daya
- https://dvlp.bpjs-kesehatan.go.id:8888/trust-mark/portal.html

## Lisensi
- Aplikasi ini open source dengan lisensi [MIT](LICENSE).