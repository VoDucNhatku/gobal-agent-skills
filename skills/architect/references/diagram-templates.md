# Diagram Templates — khuôn Mermaid cho từng mục kiến trúc

Dữ liệu tham chiếu của `architect`. Đọc **một khuôn** khi vẽ sơ đồ cho mục đó — không nạp cả file.
Mọi sơ đồ dùng khối ```` ```mermaid ```` (GitHub render sẵn; VS Code cần extension Markdown Preview
Mermaid Support). Ràng buộc: `../../_shared/rules/architecture-integrity.md` §1 — **mọi node/cạnh phải
tương ứng thứ có thật** ở mode `document`, hoặc gắn `[chưa quyết]` ở mode `blueprint`.

## Quy tắc chung (áp cho mọi sơ đồ)

- **Cạnh phải mang nhãn.** Mũi tên trần không nói gì. Nhãn = giao thức + cổng + đường dẫn:
  `-->|HTTPS :443|`, `-->|TCP :5432|`, `-->|/api/*|`. Đây là ranh giới giữa sơ đồ thật và filler.
- **Nhãn node có ký tự đặc biệt phải bọc nháy kép**: `api["API (Express :4000)"]`. Ngoặc đơn không
  bọc nháy làm vỡ parser.
- Xuống dòng trong nhãn dùng `<br/>`, không dùng `\n`.
- **Không emoji** trong sơ đồ (conventions — emoji không phải icon).
- Sơ đồ > 25 node thì tách theo miền, đừng nhồi một hình. Hình không đọc được = không có hình.
- Ở `blueprint`, node/cạnh chưa chốt vẽ nét đứt: `A -.->|chưa quyết| B`.

---

## Mục 4 — System Architecture (`flowchart`)

```mermaid
flowchart TD
  browser["Browser"] -->|HTTPS :443| gw["gateway (nginx :80/:443)"]
  gw -->|"Host: app.*"| web["frontend (SPA :8080)"]
  gw -->|"/api/, /socket.io/"| api["API (Express :4000)"]
  api -->|TCP :5432| pg[("PostgreSQL 16<br/>Prisma ORM")]
  api -->|TCP :6379| redis[("Redis 7<br/>JTI blacklist / queue broker")]
  api -->|S3 API :9000| minio[("MinIO")]
  api -->|HTTPS| stripe["Stripe API"]
  worker["Worker (BullMQ)"] -->|TCP :6379| redis

  classDef ext stroke-dasharray: 4 3
  class stripe ext
```

Bắt buộc: cổng trên mọi cạnh nội bộ · datastore dùng `[( )]` · dịch vụ ngoài vẽ nét đứt.
Nguồn kiểm chứng: `docker-compose.yml`, config gateway, biến env trỏ service.

## Mục 9 — Database (`erDiagram`)

```mermaid
erDiagram
  USER ||--o{ ENROLLMENT : "has"
  COURSE ||--o{ ENROLLMENT : "has"
  COURSE ||--o{ MODULE : "contains"
  MODULE ||--o{ LESSON : "contains"
  USER ||--o{ ORDER : "places"
  ORDER |o--|| ENROLLMENT : "grants"

  USER {
    uuid id PK
    string email UK
    string password_hash
    timestamp created_at
  }
  ENROLLMENT {
    uuid id PK
    uuid user_id FK
    uuid course_id FK
    enum status "active|refunded|expired"
    uuid order_id FK "nullable"
  }
```

Ký hiệu lực lượng: `||--o{` một-nhiều · `}o--o{` nhiều-nhiều · `|o--||` không-hoặc-một.
Chỉ liệt kê **khoá + trường mang ràng buộc** trong hình; trường đầy đủ để ở bảng dưới hình.
Bắt buộc kèm dưới hình: chiến lược migration · index không tầm thường · hành vi `onDelete` ·
có soft-delete hay không (nêu rõ đã grep xác nhận). ER 29 bảng thì tách theo aggregate.
Nguồn kiểm chứng: `schema.prisma` / `models.py` / thư mục migration.

## Mục 11 — Business Flow (`sequenceDiagram`)

```mermaid
sequenceDiagram
  actor U as User
  participant FE as Frontend (AuthProvider)
  participant API as API (auth)
  participant DB as PostgreSQL
  participant R as Redis

  U->>FE: submit email/password
  FE->>API: POST /api/auth/login
  API->>DB: find User by email
  API->>API: bcrypt.compare(password, hash)
  API->>DB: create RefreshToken (tokenHash, jti)
  API-->>FE: 200 {accessToken} + Set-Cookie refresh_token (httpOnly)
  FE->>FE: setAccessToken — in-memory only
  FE->>API: GET /api/me (Bearer accessToken)
  API->>R: check revoked jti
  API-->>FE: 200 {user}
```

Một sequence cho **một** use case, đặt tên đúng endpoint/hàm thật. Mũi tên đặc `->>` = request,
nét đứt `-->>` = response. Ca lỗi quan trọng vẽ bằng `alt`/`else`, đừng chỉ vẽ đường hạnh phúc.
Nguồn kiểm chứng: service layer, test e2e.

## Mục 6 — Request Flow (`flowchart LR`)

```mermaid
flowchart LR
  req["Request"] --> cors["cors()"] --> rl["rateLimit()"]
  rl --> auth["authenticate()<br/>JWT verify + Redis jti check"]
  auth --> val["Zod schema.parse(req.body)"]
  val --> ctrl["controller"] --> svc["service<br/>authz + business rules"]
  svc --> repo["Prisma transaction"] --> db[("DB")]
  svc -.->|throw AppError| eh["global errorHandler"]
  eh -.-> res["JSON error response"]
```

Vẽ **chuỗi middleware có thật, đúng thứ tự đăng ký**, kèm đường lỗi nét đứt. Thứ tự sai còn tệ hơn
không vẽ. Nguồn kiểm chứng: app entry (`app.js`/`main.py`) — đọc đúng thứ tự `use()`.

## Mục 12 — Dependency Graph (`flowchart`)

```mermaid
flowchart TD
  cards --> workspaces
  cards --> boards
  comments --> cards
  boards --> workspaces
  notifications --> users
  cards -.->|CYCLE| comments

  classDef cycle stroke-width:3px
  class cards,comments cycle
```

Chỉ vẽ khi tier `platform`. Giá trị nằm ở **chu trình và hub**, không ở việc liệt kê hết cạnh.
Lấy dữ liệu từ `understand-codebase` mode `scan`, đừng tự đếm.

## Chuyển trạng thái (`stateDiagram-v2`) — dùng cho mọi trường enum `status`

```mermaid
stateDiagram-v2
  [*] --> pending
  pending --> paid: webhook checkout.session.completed
  pending --> failed: payment declined
  paid --> refunded: admin refund
  failed --> [*]
```

Mỗi enum trạng thái trong DB nên có một sơ đồ này — nó biến "status có 4 giá trị" thành **luật
chuyển trạng thái**, thứ AI hay vi phạm nhất khi viết code. Cạnh phải ghi **sự kiện gây chuyển**.
Chuyển bị cấm (ví dụ `paid → pending`) ghi thành một dòng dưới hình, không vẽ.
